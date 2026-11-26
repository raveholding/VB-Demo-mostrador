"""Guía «Cómo probar esta demo» para las demos de Vincular Business.
Agrega al index.html un botón chico «Cómo probar la demo» y una ventana con los pasos (se abre sola la primera vez).
Es idempotente: si ya está, la reemplaza. Uso: python3 vb_guia.py <clave de la demo> <index.html>
Claves: mostrador, mayorista, distribuidora, gimnasio, estetica, salud, gastronomia, taller."""
import sys,json,re
G={
 'mostrador':dict(rubro='comercios de mostrador',pasos=[
   'Entrá como administrador: «Acceso», usuario <b>ADMIN</b>, PIN <b>1234</b>.',
   'En <b>Configuración → Negocio</b> ves el modelo de negocio y los datos del comercio. En <b>Adicionales para tu negocio</b> están los módulos que se suman.',
   'Probá vender en <b>Vender POS</b> (F1) y mirá Stock, Caja y el Club de clientes.',
   '<b>Ver menú público</b> muestra la tienda online conectada al stock.'],cfg='#panel/config',acc='#acceso'),
 'mayorista':dict(rubro='mayoristas',pasos=[
   'Entrá como administrador: «Acceso», usuario <b>ADMIN</b>, PIN <b>1234</b>.',
   'En <b>Configuración → Negocio</b> ves el modelo de negocio y en <b>Ventas y cobros</b> los precios por cantidad y la cuenta corriente. En <b>Adicionales para tu negocio</b> están los módulos que se suman.',
   'Probá una venta por bulto en <b>Vender POS</b> y mirá la cuenta corriente de un cliente.',
   '<b>Ver menú público</b> muestra la tienda online conectada al stock.'],cfg='#panel/config',acc='#acceso'),
 'distribuidora':dict(rubro='distribuidoras',pasos=[
   'Entrá como administrador: «Acceso», usuario <b>ADMIN</b>, PIN <b>1234</b>.',
   'En <b>Configuración → Negocio</b> ves el modelo de negocio. En <b>Adicionales para tu negocio</b> están los módulos que se suman.',
   'Recorré <b>Preventistas y rutas</b>, pedidos, reparto y cobranza.',
   '<b>Ver menú público</b> muestra la tienda online conectada al stock.'],cfg='#panel/config',acc='#acceso'),
 'gimnasio':dict(rubro='gimnasios, box y academias',pasos=[
   'Entrá como administrador: «Acceso», usuario <b>ADMIN</b>, PIN <b>1234</b>.',
   'En <b>Configuración → Rubro y módulos</b> elegí tu tipo de negocio (gimnasio, box, academia, pilates, artes marciales…) y prendé o apagá cada módulo.',
   'El menú queda armado para tu rubro: recorré socios, cuotas, clases y caja.',
   'Para ver lo que usa tu cliente, abrí <b>Ver menú público</b> o la app del socio.'],cfg='#panel/config',acc='#acceso'),
 'estetica':dict(rubro='spa, estética, barberías y tatuajes',pasos=[
   'Entrá: «Acceso», usuario <b>Administrador</b>, PIN <b>1111</b>.',
   'En <b>Configuración → Rubro del local</b> elegí spa, peluquería, uñas, tatuajes o barbería: cambian los servicios, las fichas y los textos.',
   'Recorré Agenda, Mi día y Clientes. Los módulos que no usás se apagan en Configuración.',
   '<b>Ver menú público</b> muestra el turnero que ve tu cliente.'],cfg='#panel/config',acc='#acceso'),
 'salud':dict(rubro='consultorios y clínicas',pasos=[
   'Entrá: «Acceso», usuario <b>Administrador</b>, PIN <b>1111</b>.',
   'En <b>Configuración → Rubro del local</b> elegí consultorio médico, odontológico o clínica multiespecialidad.',
   'Recorré la sala de espera, la historia clínica, el odontograma y las obras sociales.',
   '<b>Ver menú público</b> muestra los turnos online que ve el paciente.'],cfg='#panel/config',acc='#acceso'),
 'gastronomia':dict(rubro='gastronomía',pasos=[
   'Entrá como administrador: «Acceso del equipo», usuario <b>ADMIN</b>, PIN <b>1234</b>.',
   'En <b>Configuración → Tipo de negocio</b> elegí el tuyo: restaurante, parrilla, cafetería, bar, pizzería, food truck, cadena o dark kitchen.',
   'Recorré Salón, Comandas, Cocina y Fichas técnicas: cargá un pedido y cobralo.',
   '<b>Ver menú público</b> abre la carta QR que ve tu cliente.'],cfg='#panel/config',acc='#acceso'),
 'taller':dict(rubro='talleres',pasos=[
   'Elegí un perfil para entrar: el <b>Dueño</b> ve todo; jefe de taller, recepción y mecánico ven sólo lo suyo.',
   'Con el perfil Dueño, en <b>Configuración</b> ajustás los datos del taller y los servicios.',
   'Abrí una orden de trabajo por patente, presupuestala y aprobala por WhatsApp.',
   'Mirá el historial del vehículo, los repuestos y las garantías.'],cfg='',acc='')}
CSS='''#vbg-pill{position:fixed;right:16px;bottom:76px;z-index:9000;display:inline-flex;align-items:center;gap:6px;border:0;border-radius:99px;padding:8px 13px;font:600 13px/1.2 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#111;color:#fff;box-shadow:0 6px 18px rgba(0,0,0,.28);cursor:pointer}
#vbg-pill:focus-visible,#vbg-box button:focus-visible{outline:3px solid #FF7A1A;outline-offset:2px}
#vbg-ov{position:fixed;inset:0;z-index:9100;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:16px}#vbg-ov[hidden]{display:none}
#vbg-box{background:#fff;color:#111;border-radius:16px;max-width:460px;width:100%;padding:20px 20px 16px;font:400 15px/1.5 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;box-shadow:0 20px 50px rgba(0,0,0,.35);max-height:90vh;overflow:auto}
#vbg-box h2{margin:0 0 4px;font-size:19px}#vbg-box p.s{margin:0 0 10px;color:#555;font-size:13.5px}#vbg-box ol{margin:0 0 14px;padding-left:20px}#vbg-box li{margin:6px 0}
#vbg-box .r{display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap}#vbg-box button{border:1px solid #ddd;background:#fff;color:#111;border-radius:10px;padding:9px 14px;font:600 14px/1.2 inherit;cursor:pointer;min-height:40px}
#vbg-box button.p{background:#FF7A1A;border-color:#FF7A1A;color:#111}
@media print{#vbg-pill,#vbg-ov{display:none!important}}'''
def block(k):
    g=G[k]
    js='''(function(){var G=%s,K='vbg.%s';
function el(t,a,h){var e=document.createElement(t);for(var x in a)e.setAttribute(x,a[x]);if(h!=null)e.innerHTML=h;return e;}
function open(){ov.hidden=false;var b=ov.querySelector('button.p')||ov.querySelector('button');b&&b.focus();try{localStorage.setItem(K,'1');}catch(e){}}
function close(){ov.hidden=true;pill.focus();}
var pill=el('button',{id:'vbg-pill',type:'button','aria-haspopup':'dialog'},'💡 Cómo probar la demo');
var ov=el('div',{id:'vbg-ov',role:'dialog','aria-modal':'true','aria-labelledby':'vbg-t'});ov.hidden=true;
var btns=(G.cfg?'<button type="button" class="p" data-v="cfg">Ir a Configuración</button>':'')+'<button type="button" data-v="ok"'+(G.cfg?'':' class="p"')+'>Entendido</button>';
ov.innerHTML='<div id="vbg-box"><h2 id="vbg-t">Cómo probar esta demo</h2><p class="s">Demo de '+G.rubro+' con datos de ejemplo: podés tocar todo, nada es real.</p><ol>'+G.pasos.map(function(p){return '<li>'+p+'</li>';}).join('')+'</ol><div class="r">'+btns+'</div></div>';
ov.addEventListener('click',function(e){if(e.target===ov)return close();var b=e.target.closest('button');if(!b)return;
 if(b.dataset.v==='cfg'){var logged=/^#panel\\//.test(location.hash);location.hash=logged?G.cfg:G.acc;}close();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!ov.hidden)close();});
pill.addEventListener('click',open);
function mount(){document.body.appendChild(pill);document.body.appendChild(ov);var seen=false;try{seen=localStorage.getItem(K)==='1';}catch(e){}if(!seen)setTimeout(open,1500);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();})();'''%(json.dumps(dict(rubro=g['rubro'],pasos=g['pasos'],cfg=g['cfg'],acc=g['acc']),ensure_ascii=False),k)
    return '<!--vb-guia--><style>'+CSS+'</style><script>'+js+'</script><!--/vb-guia-->'
def apply(k,path):
    h=open(path,encoding='utf8').read()
    h=re.sub(r'<!--vb-guia-->.*?<!--/vb-guia-->','',h,flags=re.S)
    i=h.rfind('</body>');assert i>0,path
    h=h[:i]+block(k)+'\n'+h[i:]
    open(path,'w',encoding='utf8').write(h)
if __name__=='__main__':
    apply(sys.argv[1],sys.argv[2]);print('guía',sys.argv[1],'→',sys.argv[2])
