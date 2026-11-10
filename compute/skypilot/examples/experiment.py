"""A tiny dependency-free remote-compute and artifact-integrity smoke test."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(directory):
    directory=Path(directory)
    manifest=json.loads((directory/'manifest.json').read_text())
    if set(manifest)!= {'metrics.json','predictions.csv'}:
        raise ValueError('Unexpected artifact manifest')
    for name,expected in manifest.items():
        if digest(directory/name)!=expected:raise ValueError('Artifact checksum mismatch: '+name)
    metrics=json.loads((directory/'metrics.json').read_text())
    with (directory/'predictions.csv').open() as source:
        rows=list(csv.DictReader(source))
    if not rows:raise ValueError('Missing predictions')
    calculated=sum(abs(float(r['actual'])-float(r['prediction'])) for r in rows)/len(rows)
    if not math.isclose(calculated,metrics['candidate_mae'],rel_tol=1e-12,abs_tol=1e-12):
        raise ValueError('Prediction/metric mismatch')
    return {'verified':True,'metrics':metrics,'sha256':manifest}


def experiment(source,directory):
    source=Path(source);directory=Path(directory)
    if directory.exists():raise ValueError('Choose a fresh output directory')
    with source.open() as data:
        rows=[(float(r['x']),float(r['y'])) for r in csv.DictReader(data)]
    if len(rows)<=24 or not all(math.isfinite(v) for r in rows for v in r):
        raise ValueError('Need more than 24 finite observations')
    train,test=rows[:24],rows[24:]
    mean_x=sum(x for x,_ in train)/len(train);mean_y=sum(y for _,y in train)/len(train)
    denominator=sum((x-mean_x)**2 for x,_ in train)
    if denominator==0:raise ValueError('Training inputs have no variation')
    slope=sum((x-mean_x)*(y-mean_y) for x,y in train)/denominator
    intercept=mean_y-slope*mean_x
    predictions=[(y,intercept+slope*x) for x,y in test]
    metrics={'train_rows':len(train),'test_rows':len(test),'baseline_mae':sum(abs(y-mean_y) for _,y in test)/len(test),
             'candidate_mae':sum(abs(y-p) for y,p in predictions)/len(test),
             'slope':slope,'intercept':intercept,'input_sha256':digest(source),
             'claim':'Synthetic compute smoke test; no generalization claim.'}
    directory.mkdir(parents=True)
    with (directory/'predictions.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['actual','prediction']);writer.writerows(predictions)
    (directory/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
    (directory/'manifest.json').write_text(json.dumps({name:digest(directory/name) for name in ('metrics.json','predictions.csv')},indent=2)+'\n')
    return verify(directory)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('data.csv'))
    parser.add_argument('--output',type=Path,default=Path('output'))
    parser.add_argument('--verify',type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.verify) if args.verify else experiment(args.input,args.output),indent=2))


if __name__=='__main__':main()
