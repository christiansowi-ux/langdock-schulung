const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const box={module:{exports:{}}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../public/assets/demo-core.js'),'utf8'),box);const C=box.module.exports;
test('Vier beschriebene Einsätze führen zu vier verschiedenen Lernhinweisen',()=>{
  for(const [scenario,kind] of Object.entries({text:'normal',people:'high',emotion:'stop',unknown:'open'})){
    let r=C.risk({scenario,role:'user',personal:false,guess:kind});assert.equal(r.kind,kind);assert.equal(r.match,true);
  }
});
test('Anbieterrolle oder Testdaten heben das Verbot nicht auf',()=>{
  for(const role of ['provider','user'])for(const personal of [true,false])assert.equal(C.risk({scenario:'emotion',role,personal}).kind,'stop');
  assert.match(C.risk({scenario:'text',role:'provider'}).role,/Anbieterrolle/);
  assert.match(C.risk({scenario:'text',role:'user'}).role,/Betreiberrolle/);
});
test('Falsche Vermutung bleibt falsch und unbekannter Zweck wird nicht geraten',()=>{
  assert.equal(C.risk({scenario:'people',guess:'normal'}).match,false);
  assert.equal(C.risk({scenario:'unknown',guess:'high'}).kind,'open');
});
test('Nur ein klarer Hinweis vor Interaktion erreicht das Demo-Ziel',()=>{
  for(const label of ['human','vague','clear'])for(const place of ['start','late']){
    assert.equal(C.transparency({label,place}).complete,label==='clear'&&place==='start');
  }
});
test('Prompt reagiert auf Fakten und Grenzen; alle vier Bausteine nötig',()=>{
  const none=C.prompt({},'tabea');const facts=C.prompt({context:true},'tabea');const full=C.prompt({context:true,limits:true,audience:true,format:true},'tabea');
  assert.notEqual(none.output,facts.output);assert.match(facts.output,/nicht belegt/);assert.doesNotMatch(full.output,/nicht belegt/);
  assert.equal(full.complete,true);assert.equal(facts.complete,false);assert.match(full.instruction,/Erfinde keine/);
  assert.notEqual(C.prompt({context:true},'ingo').output,C.prompt({context:true},'carmen').output);
});
test('Alle 16 Kombinationen der Assistenzregeln werden konsistent geprüft',()=>{
  for(let mask=0;mask<16;mask++){
    let s={ask:!!(mask&1),source:!!(mask&2),separate:!!(mask&4),honest:!!(mask&8)};let r=C.agent(s);
    assert.equal(r.complete,mask===15);assert.equal(r.passed,Number(s.ask&&s.honest)+Number(s.source)+Number(s.separate&&s.honest));
    assert.equal(r.tests.length,3);assert.match(C.instruction(s),s.honest?/Erteile keine rechtliche Freigabe/:/möglichst eindeutig/);
  }
});
