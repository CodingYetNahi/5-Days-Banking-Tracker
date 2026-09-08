const test=require('node:test'),assert=require('node:assert/strict');const {elapsedParts,timerState}=require('../timer');
test('calendar elapsed parts include all units',()=>assert.deepEqual(elapsedParts('2024-01-01T00:00:00Z','2025-02-03T04:05:06Z'),{years:1,months:1,days:2,hours:4,minutes:5,seconds:6,totalDays:399}));
test('future reference clamps to zero',()=>assert.equal(elapsedParts('2030-01-01','2029-01-01').totalDays,0));
test('official implementation stops at configured date',()=>{const s=timerState({reference_date:'2024-01-01Z',implementation_date:'2024-01-03Z',status:'officially_implemented',is_running:0},new Date('2026-01-01Z'));assert.equal(s.stopped,true);assert.equal(s.elapsed.totalDays,2);assert.match(s.message,/Congratulations/)});
test('official state requires implementation date',()=>assert.throws(()=>timerState({reference_date:'2024-01-01',status:'officially_implemented',is_running:0}),/required/));
