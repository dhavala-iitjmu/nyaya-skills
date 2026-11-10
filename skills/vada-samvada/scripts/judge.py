"""Aggregate supplied rubric assessments, not a substitute for evidence evaluation."""
import argparse
import json
import math
from pathlib import Path


def number(value,minimum=0,maximum=100):
    if type(value) not in (int,float) or not math.isfinite(value) or not minimum<=value<=maximum:raise ValueError('Invalid bounded number')
    return value


def evaluate(body):
    criteria=body['criteria'];assessments=body.get('assessments',[])
    threshold=number(body.get('threshold',80));remaining=body.get('remaining_turns',1)
    if type(remaining) is not int or remaining<0:raise ValueError('Invalid remaining_turns')
    if not isinstance(criteria,list) or not 1<=len(criteria)<=100 or not isinstance(assessments,list):raise ValueError('Supply a bounded rubric and assessments')
    ids=[c['id'] for c in criteria]
    if any(not isinstance(i,str) or not i for i in ids) or len(set(ids))!=len(ids):raise ValueError('Unique criterion IDs required')
    judged={}
    for item in assessments:
        if item['id'] not in ids or item['id'] in judged:raise ValueError('Unknown or duplicate assessment')
        if item.get('status') not in ('pass','fail','unknown'):raise ValueError('Invalid judgment status')
        if not isinstance(item.get('reason'),str) or not item['reason'].strip():raise ValueError('A reason is required')
        evidence=item.get('evidence',[])
        if not isinstance(evidence,list) or any(not isinstance(e,str) or not e.strip() for e in evidence):raise ValueError('Evidence must contain nonempty references')
        judged[item['id']]=item
    findings=[];weighted=0.;weights=0.;unknown=False;failed=False;quality_complete=True
    for criterion in criteria:
        mandatory=criterion.get('mandatory',False)
        if type(mandatory) is not bool:raise ValueError('mandatory must be boolean')
        weight=number(criterion.get('weight',0),maximum=10000)
        item=judged.get(criterion['id']);status=item['status'] if item else 'unknown'
        if item and status!='unknown' and not item.get('evidence'):status='unknown'
        if mandatory:
            unknown|=status=='unknown';failed|=status=='fail'
        if weight:
            weights+=weight
            if not item or status=='unknown' or item.get('score') is None:quality_complete=False;unknown=True
            else:weighted+=weight*number(item['score'])
        findings.append({'id':criterion['id'],'status':status,'mandatory':mandatory})
    if not any(c.get('mandatory',False) or c.get('weight',0)>0 for c in criteria):raise ValueError('Rubric has no acceptance criteria')
    score=weighted/weights if weights and quality_complete else None
    accepted=not failed and not unknown and (not weights or score>=threshold)
    decision='graduate' if accepted else 'escalate' if remaining==0 else 'revise' if failed or not unknown else 'clarify'
    return {'decision':decision,'accepted':accepted,'quality_score':score,'threshold':threshold if weights else None,'findings':findings,'assessment_only':True}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.input.stat().st_size>1000000:raise ValueError('Input too large')
    result=json.dumps(evaluate(json.loads(args.input.read_text())),indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(result)
    else:print(result,end='')

if __name__=='__main__':main()
