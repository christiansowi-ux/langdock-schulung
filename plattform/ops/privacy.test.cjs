const test=require('node:test');const assert=require('node:assert/strict');const vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');const context={module:{exports:{}}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../public/assets/privacy-core.js'),'utf8'),context);const C=context.module.exports;
test('All fixed cases distinguish correct answers and return feedback for every option',()=>{
 for(const kind of ['detective','inbox'])for(const [i,row]of C[kind].entries()){
  const options=kind==='detective'?C.categories:row.options;
  for(let j=0;j<options.length;j++){const r=C.answer(kind,i,j);assert.equal(r.correct,j===row.answer);assert.ok(r.feedback.length>30);}
  assert.ok(row.slide>=1&&row.slide<=74);
 }
 assert.equal(C.answer('inbox',100,0),null);assert.equal(C.answer('detective',0,-1),null);assert.equal(C.answer('inbox',0,1.2),null);
});
test('Pseudonymization, indirect identification, ordinary photo and diagnosis stay distinct',()=>{
 assert.equal(C.categories[C.detective.find(x=>x.id==='code').answer],'Pseudonymisiert · weiterhin personenbezogen');
 assert.equal(C.detective.find(x=>x.id==='role').answer,0);assert.equal(C.detective.find(x=>x.id==='photo').answer,0);
 assert.equal(C.detective.find(x=>x.id==='health').answer,3);assert.equal(C.detective.find(x=>x.id==='stats').answer,2);
});
for(const profile of ['ingo','carmen','tabea'])test(profile+': all 512 field selections enforce data need and avoid empty-prompt success',()=>{
 const f=C.fields(profile);assert.equal(f.length,9);
 for(let mask=0;mask<512;mask++){
  const selected=f.filter((_,i)=>mask&(1<<i)).map(x=>x.id),r=C.minimize(profile,selected);
  assert.equal(r.complete,mask===7);assert.equal(r.kept.length,selected.length);
  if((mask&7)!==7)assert.match(r.output,/fehlen/);else assert.equal(r.output,C.jobs[profile].output);
 }
 assert.equal(C.minimize(profile,['fact0','fact1','fact2','fact2','unknown']).complete,true);
 assert.equal(C.minimize(profile,null).complete,false);
});
test('No factual dependence on unnecessary personal fields',()=>{
 for(const p of Object.keys(C.jobs)){const minimal=C.minimize(p,['fact0','fact1','fact2']),all=C.minimize(p,C.fields(p).map(x=>x.id));assert.equal(minimal.output,all.output);assert.equal(all.extra.length,6);assert.equal(all.complete,false);}
});
