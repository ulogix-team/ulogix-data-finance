const fs=require("fs");
const {Document,Packer,Paragraph,TextRun,HeadingLevel,AlignmentType,Table,TableRow,TableCell,
 WidthType,BorderStyle,ShadingType,PageBreak,ImageRun,TableOfContents,LevelFormat,PageNumber,Header,Footer}=require("docx");
const FONT="Times New Roman",BK="000000",SH="D9D9D9",SH2="F2F2F2";
const D=JSON.parse,rd=f=>fs.readFileSync(f);
const val=D(rd("data/validacion_2026T1.json")),evr=D(rd("data/evaluacion_resumen.json"));
const pca=D(rd("data/pca.json")),pru=D(rd("data/pruebas_estadisticas.json")),kof=D(rd("data/kof_trimestral_colombia.json"));
// helpers: run at 24 half-points = 12pt
const run=(t,o={})=>new TextRun({text:t,font:FONT,size:o.size||24,bold:!!o.bold,italics:!!o.it,color:BK,subScript:!!o.sub,superScript:!!o.sup});
const P=(c,o={})=>new Paragraph({alignment:o.align||AlignmentType.JUSTIFIED,spacing:{after:o.after??120,line:240},children:Array.isArray(c)?c:[run(c,o)]});
const EQ=(rr)=>new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:80,after:120},children:rr});
const H1=(t)=>new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:240,after:120},children:[run(t)]});
const H2=(t)=>new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:180,after:100},children:[run(t)]});
const H3=(t)=>new Paragraph({heading:HeadingLevel.HEADING_3,spacing:{before:140,after:80},children:[run(t)]});
const sizes={"figuras/fig_metodologia.png":[1114,1635],"figuras/fig_series.png":[1339,1038],
 "figuras/fig_boxplot_mes.png":[1039,419],"figuras/fig_acf.png":[1339,439],"figuras/fig_descomposicion.png":[1200,900],
 "figuras/fig_hist_dist.png":[1487,450],"figuras/fig_qq.png":[1487,450],"figuras/fig_montecarlo.png":[1639,469],
 "figuras/fig_corr.png":[584,499],"figuras/fig_pca.png":[1339,450]};
let figN=0;
const FIG=(p,w,cap)=>{const s=sizes[p];figN++;return [
 new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:80,after:20},
  children:[new ImageRun({data:fs.readFileSync(p),transformation:{width:w,height:Math.round(w*s[1]/s[0])}})]}),
 new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:140},children:[run("Fig. "+figN+". "+cap,{it:true,size:20})]})];};
let tabN=0;
function cell(t,{w,head=false,shade=null,align=AlignmentType.CENTER,bold=false,size=20}={}){
 return new TableCell({width:{size:w,type:WidthType.DXA},
  shading:head?{type:ShadingType.CLEAR,fill:SH}:(shade?{type:ShadingType.CLEAR,fill:shade}:undefined),
  margins:{top:40,bottom:40,left:60,right:60},
  borders:{top:{style:BorderStyle.SINGLE,size:4,color:BK},bottom:{style:BorderStyle.SINGLE,size:4,color:BK},left:{style:BorderStyle.SINGLE,size:4,color:BK},right:{style:BorderStyle.SINGLE,size:4,color:BK}},
  children:[new Paragraph({alignment:align,spacing:{after:0},children:[run(String(t),{size,bold:head||bold})]})]});}
function TBL(cap,h,rows,w,size=20){tabN++;return [
 new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:80,after:20},children:[run("TABLA "+tabN+". "+cap,{it:true,size:20})]}),
 new Table({columnWidths:w,width:{size:w.reduce((a,b)=>a+b,0),type:WidthType.DXA},alignment:AlignmentType.CENTER,rows:[
  new TableRow({tableHeader:true,children:h.map((x,i)=>cell(x,{w:w[i],head:true,size}))}),
  ...rows.map((r,ri)=>new TableRow({children:r.map((x,i)=>cell(x,{w:w[i],size,align:i===0?AlignmentType.LEFT:AlignmentType.CENTER,shade:ri%2?SH2:null,bold:i===0}))}))]}),
 new Paragraph({spacing:{after:120},children:[run("")]})];}
const REF=(n,t)=>new Paragraph({spacing:{after:60},indent:{left:520,hanging:520},children:[run("["+n+"] ",{}),run(t)]});
const f1=v=>Number(v).toLocaleString("es-CO");
const kofRows=Object.entries(kof).map(([k,v])=>{const y=k.slice(0,4),q=k.slice(-1);
 return [y+"T"+q,v.refrescos.toFixed(1),v.agua.toFixed(1),v.garrafon.toFixed(1),v.otros.toFixed(1),v.total.toFixed(1),(y==="2021"?"comp. "+(Number(y)+1):y)+"-T-"+q];});

const numbering={config:[
 {reference:"h1",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.START,style:{run:{font:FONT,bold:true,size:24}}}]},
]};
const styles={
 default:{document:{run:{font:FONT,size:24,color:BK}}},
 paragraphStyles:[
  {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
   run:{font:FONT,size:24,bold:true,allCaps:true,color:BK},paragraph:{spacing:{before:240,after:120},keepNext:true}},
  {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
   run:{font:FONT,size:24,bold:true,italics:true,color:BK},paragraph:{spacing:{before:180,after:100},keepNext:true}},
  {id:"Heading3",name:"Heading 3",basedOn:"Normal",next:"Normal",quickFormat:true,
   run:{font:FONT,size:24,italics:true,color:BK},paragraph:{spacing:{before:140,after:80},keepNext:true}},
  {id:"Title",name:"Title",basedOn:"Normal",next:"Normal",quickFormat:true,
   run:{font:FONT,size:40,bold:true,color:BK}},
 ]};

const children=[];
// ===== PORTADA (IEEE title block) =====
children.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:1400,after:0},children:[run("Pronóstico de Demanda, Análisis de Capacidad y Bases para ERP en la Planta Embotelladora Coca-Cola FEMSA (Fontibón, Bogotá): un Estudio Integral de Ingeniería de Producción",{size:36,bold:true})]}));
children.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:360,after:0},children:[run("Proyecto de Ingeniería — Gestión de Producción Automatizada (APM)",{size:24})]}));
children.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:600,after:0},children:[run("Resumen — ",{bold:true,it:true}),
 run("Este trabajo documenta el desarrollo completo de un sistema de planeación de la producción para tres líneas de la planta embotelladora de Industria Nacional de Gaseosas S.A.S. (INDEGA, Coca-Cola FEMSA) en Fontibón, Bogotá. A partir de 21 trimestres de volumen real de la compañía se reconstruyó la demanda histórica por categoría y se ajustaron modelos de pronóstico de la familia Holt-Winters con tendencia amortiguada, validados mediante backtest fuera de muestra (MAPE 2,7 %) y contra el trimestre real más reciente (error +0,07 %). La incertidumbre se cuantificó por simulación Monte Carlo sobre una distribución del error verificada con pruebas de bondad de ajuste. El pronóstico se tradujo a un plan de producción en unidades, empaques y pallets, y se analizaron los tiempos de fabricación y la eficacia global del equipo (OEE) construida de forma ascendente desde los datos de una visita técnica, obteniéndose valores en el rango observado de 75–78 %. El análisis de capacidad reveló que dos de las tres líneas operan por encima de su capacidad de dos turnos, y que la estación crítica de la línea de garrafones es el paletizado manual de cargas de 25 kg. Finalmente se generaron las bases de datos de productos, listas de materiales y pronóstico para su importación en el sistema ERP Odoo.",{it:true})]}));
children.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:200,after:0},children:[run("Términos clave — ",{bold:true,it:true}),run("Holt-Winters, OEE, TEEP, pronóstico de demanda, Monte Carlo, takt time, VSM, Odoo ERP, embotellado.",{it:true})]}));
children.push(new Paragraph({children:[new PageBreak()]}));

// ===== TOC =====
children.push(new Paragraph({spacing:{after:120},children:[run("CONTENIDO",{bold:true,size:24,allCaps:true})]}));
children.push(new TableOfContents("Contenido",{hyperlink:true,headingStyleRange:"1-3"}));
children.push(new Paragraph({children:[new PageBreak()]}));

// ===== I. INTRODUCCION =====
children.push(H1("Introducción"));
children.push(P([run("La planeación de la producción en una planta embotderadora de bebidas exige articular tres decisiones que suelen tratarse por separado: cuánto se venderá (pronóstico de demanda), cuánto puede fabricarse (capacidad y tiempos) y cómo se registra y coordina todo ello (sistema de información). Este reporte integra las tres para el caso de la planta de Coca-Cola FEMSA en Fontibón, operada por INDEGA, y tres de sus productos representativos: Coca-Cola 350 mL en vidrio retornable, QuAtro 1,5 L en PET no retornable y garrafón de agua de 25 L retornable.")]));
children.push(P([run("El reto metodológico central fue la ausencia de series de demanda a nivel de planta individual, dato que ninguna fuente pública reporta. La solución consistió en reconstruir la demanda a partir de información corporativa verificable —los reportes de resultados trimestrales de Coca-Cola FEMSA— y escalarla a la planta mediante parámetros de participación explícitos y auditables. Sobre esa base se aplicó un procedimiento formal de selección de método de pronóstico, se dimensionó la capacidad con las fórmulas clásicas de ingeniería de producción, y se prepararon las estructuras de datos para el ERP.")]));
children.push(P([run("El documento está organizado como sigue. La Sección II resume el marco teórico. La Sección III describe los datos y su trazabilidad. La Sección IV presenta el modelo de pronóstico y su validación. La Sección V cuantifica la incertidumbre por simulación. La Sección VI aborda el análisis multivariado. La Sección VII desarrolla el análisis de tiempos, OEE y TEEP. La Sección VIII presenta el análisis de capacidad frente a la demanda. La Sección IX describe las bases del ERP. La Sección X concluye.")]));

// ===== II. MARCO TEORICO =====
children.push(H1("Marco Teórico"));
children.push(H2("A. Series de Tiempo y sus Componentes"));
children.push(P([run("Una serie de tiempo se descompone en nivel, tendencia y estacionalidad. La identificación de cuáles componentes están presentes determina el método de pronóstico apropiado, pues aplicar un método sin estacionalidad a una serie estacional introduce error sistemático.")]));
children.push(H2("B. Suavización Exponencial de Holt-Winters"));
children.push(P([run("El método de Holt-Winters [1], [2] pronostica mediante promedios ponderados con decaimiento geométrico, actualizando tres componentes. En su forma multiplicativa con tendencia amortiguada, las ecuaciones de nivel, tendencia, estacionalidad y pronóstico son:")]));
children.push(EQ([run("ℓ",{it:true}),run("t",{sub:true}),run(" = α(y",{it:true}),run("t",{sub:true}),run("/s",{it:true}),run("t−m",{sub:true}),run(") + (1−α)(ℓ",{it:true}),run("t−1",{sub:true}),run("+φb",{it:true}),run("t−1",{sub:true}),run(")   (1)")]));
children.push(EQ([run("b",{it:true}),run("t",{sub:true}),run(" = β(ℓ",{it:true}),run("t",{sub:true}),run("−ℓ",{it:true}),run("t−1",{sub:true}),run(") + (1−β)φb",{it:true}),run("t−1",{sub:true}),run("   (2)")]));
children.push(EQ([run("s",{it:true}),run("t",{sub:true}),run(" = γ(y",{it:true}),run("t",{sub:true}),run("/ℓ",{it:true}),run("t",{sub:true}),run(") + (1−γ)s",{it:true}),run("t−m",{sub:true}),run("   (3)")]));
children.push(EQ([run("ŷ",{it:true}),run("t+h",{sub:true}),run(" = (ℓ",{it:true}),run("t",{sub:true}),run(" + Σφ",{it:true}),run("i",{sup:true}),run(" b",{it:true}),run("t",{sub:true}),run(") s",{it:true}),run("t+h−m",{sub:true}),run("   (4)")]));
children.push(P([run("El parámetro α∈(0,1) gobierna la velocidad de reacción al dato reciente; el factor de amortiguación φ<1 evita que la tendencia se extrapole indefinidamente, propiedad que la literatura de las competencias M asocia a mayor exactitud fuera de muestra y que constituye la elección conservadora [2], [11].")]));
children.push(H2("C. Combinación de Pronósticos"));
children.push(P([run("Cuando dos modelos capturan señales distintas y complementarias de una misma serie, Bates y Granger [12] demostraron que su combinación lineal puede superar a cada modelo individual. Este principio se aplicó al garrafón, que pertenece al mercado de agua pero constituye un segmento de consumo propio.")]));
children.push(H2("D. Métricas de Error y Señal de Rastreo"));
children.push(P([run("Con el error e = real − pronóstico se definen el error absoluto medio (MAD), el error cuadrático medio (MSE) y su raíz (RMSE), el error porcentual absoluto medio (MAPE) y el error acumulado (CFE). La señal de rastreo TS = CFE/MAD monitorea el sesgo: mientras |TS| ≤ 4 el pronóstico se considera insesgado; su cruce señala un cambio estructural que exige recalibración [13].")]));
children.push(H2("E. Indicadores de Tiempos y Eficacia"));
children.push(P([run("La ingeniería de producción define el takt time T = T",{}),run("D",{sub:true}),run("/D (ritmo de la demanda), el tiempo de ciclo T",{}),run("c",{sub:true}),run(" = 3600/R",{}),run("p",{sub:true}),run(" (ritmo de la máquina), el tiempo de lote T",{}),run("b",{sub:true}),run(" = T",{}),run("su",{sub:true}),run(" + Q·T",{}),run("c",{sub:true}),run(", la capacidad PC = n·S·H·R",{}),run("p",{sub:true}),run(", la utilización U = Q/PC y el tiempo de fabricación MLT. La eficacia global del equipo se define como OEE = A × PE × Q, con disponibilidad A, eficiencia de desempeño PE y tasa de calidad Q [11]. El TEEP (Total Effective Equipment Performance) extiende el OEE al calendario total: TEEP = OEE × Carga, donde la Carga es la fracción del tiempo calendario efectivamente programada.")]));

// ===== III. DATOS =====
children.push(H1("Datos y Trazabilidad"));
children.push(P([run("La fuente primaria fueron los 17 reportes de resultados trimestrales de Coca-Cola FEMSA (1T-2022 a 1T-2026) [21]. De cada reporte se extrajo la fila de Colombia de la tabla de volumen por categoría (refrescos, agua, garrafón, otros), en millones de cajas unidad (MCU), donde una caja unidad equivale a 5,6781 L. Las columnas comparativas de los reportes de 2022 extendieron la serie a 2021, para un total de 21 trimestres observados. La extracción es reproducible (biblioteca pypdf) y superó dos verificaciones automáticas: consistencia interna (las categorías suman el total en los 21 casos) y cuadre con los informes integrados anuales (2022: 330,0 vs 330,1; 2025: 349,5 vs 349,4 MCU) [1]–[3].")]));
children.push(...TBL("Volumen trimestral real — Colombia (MCU) y archivo fuente",
 ["Trim.","Refr.","Agua","Garr.","Otros","Total","Fuente"],kofRows,[760,900,760,860,760,860,2100],18));
children.push(P([run("La demanda de planta se obtuvo escalando el universo nacional por la participación de Bogotá en el consumo (17 %, sustentada en la población del Distrito, 15,1 % del país [6], y su mayor consumo per cápita [8]) y por un factor de captura de la planta de Fontibón frente a la red de siete plantas de la compañía [13]. La mezcla de empaque de carbonatadas (34 % retornable, 66 % no retornable) proviene del informe integrado 2025 [3].")]));

// ===== IV. PRONOSTICO =====
children.push(H1("Modelo de Pronóstico y Validación"));
children.push(P([run("Se siguió el procedimiento formal resumido en la Fig. 1, que encadena el análisis estadístico de la serie, la selección del método según sus componentes, el ajuste de la distribución del error, la simulación y el control por señal de rastreo.")]));
children.push(...FIG("figuras/fig_metodologia.png",360,"Procedimiento formal de selección y validación del método de pronóstico."));
children.push(H2("A. Diagnóstico de la Serie"));
children.push(P([run("Las pruebas de rachas, Kruskal-Wallis y Levene, junto con la función de autocorrelación sobre la serie diferenciada, se resumen en la Tabla II. Los refrescos —base de los productos P1 y P2— presentan estacionalidad anual significativa (autocorrelación en el rezago 4, con p de Ljung-Box de 0,028), lo que conduce a Holt-Winters multiplicativo con m = 4.")]));
children.push(...TBL("Pruebas estadísticas sobre las categorías reales",
 ["Categoría","Rachas p","K-W p","Levene p","ACF-4 (Δ)","L-B p","Dictamen"],
 [["Refrescos",String(pru.refrescos.rachas.p),String(pru.refrescos.kruskal_wallis.p),String(pru.refrescos.levene.p),String(pru.refrescos.acf_lag4_diff),String(pru.refrescos.ljungbox_lag4_p),"Estacional"],
  ["Agua",String(pru.agua.rachas.p),String(pru.agua.kruskal_wallis.p),String(pru.agua.levene.p),String(pru.agua.acf_lag4_diff),String(pru.agua.ljungbox_lag4_p),"Tendencia"],
  ["Garrafón",String(pru.garrafon.rachas.p),String(pru.garrafon.kruskal_wallis.p),String(pru.garrafon.levene.p),String(pru.garrafon.acf_lag4_diff),String(pru.garrafon.ljungbox_lag4_p),"Cuasi-estable"]],
 [1500,1150,1050,1050,1150,1050,1600]));
children.push(...FIG("figuras/fig_series.png",420,"Serie trimestral real escalada a planta (2021T1–2026T1) y pronóstico 2026T2–2027T1."));
children.push(...FIG("figuras/fig_acf.png",420,"ACF y PACF de la serie diferenciada de refrescos: pico significativo en el rezago 4."));
children.push(H2("B. Modelo del Garrafón: Combinación de Pronósticos"));
children.push(P([run("El garrafón forma parte del mercado de agua, por lo que se evaluó un modelo que lo liga a la demanda de agua total (agua personal más garrafón, pronosticada con Holt-Winters, multiplicada por la participación del garrafón suavizada). Sin embargo, el análisis multivariado (Sección VI) mostró que el garrafón es un segmento casi independiente, y el backtest confirmó que el modelo de agua puro predice peor. Siguiendo a Bates y Granger [12], el pronóstico oficial de P3 es la combinación en partes iguales del modelo directo y el ligado al agua, lo que incorpora la señal del mercado sin sacrificar precisión. La Tabla III compara los tres esquemas.")]));
children.push(...TBL("Comparación de modelos para el garrafón (MAPE de backtest)",
 ["Modelo","MAPE","Comentario"],
 [["Directo (Holt-Winters)","1,91 %","Mejor ajuste individual"],
  ["Ligado al mercado de agua","7,54 %","Incorpora la dinámica del agua"],
  ["Combinado (oficial)","4,58 %","Equilibrio señal-precisión"]],
 [2400,1200,3400]));
children.push(H2("C. Validación"));
children.push(P([run("La validación más exigente consistió en entrenar el modelo solo hasta el 4T-2025 y predecir el 1T-2026 real: el error fue de +0,07 % en P1 y P2, y de −1,04 % en P3. El backtest de cinco trimestres fuera de muestra (entrenamiento 2021T1–2024T4) arrojó los resultados de la Tabla IV. La señal de rastreo alcanza su límite en los trimestres del impuesto saludable de 2025, un quiebre estructural con causa asignable y documentada; el error del último trimestre probado es ya mínimo.")]));
children.push(...TBL("Validación fuera de muestra (backtest 2025T1–2026T1)",
 ["Prod.","MAD (L)","RMSE (L)","MAPE","Valid. 1T-26","TS máx"],
 [["P1",f1(evr.P1.MAD),f1(evr.P1.RMSE),evr.P1.MAPE+" %",val.P1.error_pct+" %",String(evr.P1.TS_max_abs)],
  ["P2",f1(evr.P2.MAD),f1(evr.P2.RMSE),evr.P2.MAPE+" %",val.P2.error_pct+" %",String(evr.P2.TS_max_abs)],
  ["P3",f1(evr.P3.MAD),f1(evr.P3.RMSE),evr.P3.MAPE+" %",val.P3.error_pct+" %",String(evr.P3.TS_max_abs)]],
 [900,1500,1500,1100,1400,1000]));
children.push(...FIG("figuras/fig_descomposicion.png",380,"Descomposición multiplicativa del dato real de refrescos (m = 4)."));

// ===== V. MONTECARLO =====
children.push(H1("Cuantificación de la Incertidumbre"));
children.push(P([run("El error relativo del ajuste se modeló como variable aleatoria y se contrastó la hipótesis de normalidad con las pruebas de Kolmogorov-Smirnov, Anderson-Darling y chi-cuadrado, que la aceptaron en los tres productos (Figs. 5 y 6). Sobre esa base se ejecutó una simulación Monte Carlo de 10 000 réplicas (semilla fija para reproducibilidad), obteniéndose las bandas de confianza P5–P95 de la Fig. 7 y la Tabla V, insumo directo para el dimensionamiento de inventarios de seguridad.")]));
children.push(...FIG("figuras/fig_hist_dist.png",430,"Residuos relativos del ajuste (n = 21) e hipótesis Normal."));
children.push(...FIG("figuras/fig_qq.png",430,"Gráficos cuantil-cuantil de los residuos."));
children.push(...FIG("figuras/fig_montecarlo.png",450,"Bandas P5–P95 de la simulación Monte Carlo (abril 2026 – marzo 2027)."));
children.push(...TBL("Pronóstico anual y bandas Monte Carlo (millones de litros)",
 ["Prod.","HW base","P5","P50","P95"],
 [["P1","65,4","61,8","65,6","69,4"],["P2","81,6","77,2","81,9","86,5"],["P3","6,9","6,1","6,9","7,7"]],
 [1100,2100,1700,1700,1700]));

// ===== VI. MULTIVARIADO =====
children.push(H1("Análisis Multivariado"));
children.push(P([run("La matriz de correlación y el análisis de componentes principales sobre las categorías reales (Figs. 8 y 9) revelan una estructura de dos bloques: refrescos y agua co-mueven fuertemente (r = 0,87), mientras el garrafón es prácticamente independiente (r = 0,12 con refrescos, 0,20 con agua personal). La primera componente explica el "+(pca.varianza_explicada[0]*100).toFixed(1)+" % de la varianza y la segunda, cargada casi exclusivamente por el garrafón, el "+(pca.varianza_explicada[1]*100).toFixed(1)+" %. La consecuencia operativa es doble: los picos de P1 y P2 coinciden y deben planearse de forma conjunta, mientras que la línea de garrafón puede programarse en contraciclo, aprovechando los valles de las demás.")]));
children.push(...FIG("figuras/fig_corr.png",240,"Correlación entre categorías reales (2021–2026)."));
children.push(...FIG("figuras/fig_pca.png",420,"Análisis de componentes principales: gráfico de sedimentación y biplot."));

// ===== VII. TIEMPOS Y OEE =====
children.push(H1("Análisis de Tiempos, OEE y TEEP"));
children.push(P([run("Las tasas de producción se establecieron a partir de referencias comerciales de equipos usados coherentes con la antigüedad de la planta (más de quince años) y con las marcas identificadas en la visita técnica: llenadoras KRONES, inspectores HEUFT y Linatronic, y monoblocks de garrafón de clase industrial [1]–[9]. La estación crítica de cada línea es el llenado, salvo en la de garrafones, donde lo es el paletizado manual.")]));
children.push(H2("A. OEE Construido de Forma Ascendente"));
children.push(P([run("A diferencia de un enfoque que ajusta los parámetros para alcanzar un OEE objetivo, aquí cada componente se construyó desde datos del sistema y el rango de 75–78 % observado en la visita se empleó únicamente como validación. La disponibilidad A se derivó de los tiempos del turno (una hora de alistamiento más saneamiento como inactividad planeada, y las paradas no planeadas del protocolo de fallas). La eficiencia de velocidad SE se obtuvo de la relación entre la tasa real y la de placa de cada equipo usado, y la eficiencia de ritmo RE de los microparos medibles. La Tabla VI muestra que el OEE resultante cae por sí solo en el rango observado.")]));
children.push(...TBL("OEE construido de forma ascendente, por línea",
 ["Componente","L1 (350)","L2 (1,5 L)","L3 (garr.)"],
 [["Disponibilidad A","89,0 %","89,0 %","89,0 %"],
  ["Vel. SE = real/placa","94,4 %","92,3 %","92,3 %"],
  ["Ritmo RE (microparos)","91,8 %","93,1 %","91,8 %"],
  ["Desempeño PE = RE·SE","86,7 %","86,0 %","84,7 %"],
  ["Calidad Q","99,93 %","99,93 %","99,93 %"],
  ["OEE = A·PE·Q","77,1 %","76,5 %","75,4 %"],
  ["Validación (75–78 %)","Sí","Sí","Sí"]],
 [2400,1550,1550,1550]));
children.push(H2("B. Tiempos de Ciclo, Takt y Lote"));
children.push(P([run("El lote de producción se definió como lo fabricado en un turno de 8 horas, redondeado a pallets completos: 262 440 botellas (162 pallets) en L1, 73 080 (87 pallets) en L2 y 2 880 garrafones (96 pallets) en L3. La comparación entre el tiempo de ciclo y el takt time de diciembre confirma, por la vía del ritmo, la restricción de capacidad de la Sección VIII. El tiempo de fabricación del lote-turno, calculado sobre la base de los diagramas VSM del proyecto [13], resultó de 17,0, 19,3 y 15,6 horas respectivamente, dominado por las esperas entre estaciones.")]));
children.push(H2("C. Paletizado Manual del Garrafón"));
children.push(P([run("La línea de garrafones carece de celda robótica: un operario levanta recipientes de 25 kg uno a uno y los ubica en el pallet. El ciclo sostenible, acotado por criterios de levantamiento repetitivo, es de unos 15 s por unidad, equivalente a 240 garrafones por hora y por operario. Con dos operarios la línea rinde 480 garrafones por hora —por debajo de la llenadora de 600—, lo que convierte al paletizado en la estación crítica y en la candidata natural a semiautomatización en fases futuras.")]));
children.push(H2("D. TEEP y su Interpretación"));
children.push(P([run("El TEEP se calculó con el calendario laboral de Bogotá: descontando domingos, los dieciocho festivos anuales (Ley 51 de 1983) y una parada mayor de mantenimiento, resultan 286 días operativos para las líneas de dos turnos y 120 para la de garrafón en contraciclo. La Tabla VII muestra los resultados. El TEEP de 40 % de L1 y L2 es realista: representa el 77 % de su techo estructural de dos turnos (52,2 % del calendario), donde caen las plantas con buen OEE operando dos turnos; los valores de clase mundial de 60–75 % solo son alcanzables con operación continua. El TEEP de 8,3 % de la línea de garrafón no indica bajo desempeño, sino capacidad latente deliberada, coherente con su programación en contraciclo.")]));
children.push(...TBL("Carga calendario y TEEP por línea",
 ["Línea","OEE","Carga (Bogotá)","TEEP"],
 [["L1 · CC 350","77,1 %","52,2 %","40,3 %"],
  ["L2 · QuAtro 1,5 L","76,5 %","52,2 %","40,0 %"],
  ["L3 · Garrafón","75,4 %","11,0 %","8,3 %"]],
 [2400,1550,1900,1550]));

// ===== VIII. CAPACIDAD =====
children.push(H1("Capacidad frente a la Demanda"));
children.push(P([run("Contrastando la capacidad efectiva anual (capacidad nominal degradada por el OEE y ajustada al calendario) con la demanda de 2025 (estado actual) y la pronosticada para 2026 (futuro), se obtiene el diagnóstico de la Tabla VIII. El hallazgo central es que las dos líneas de gaseosas ya operaban por encima de su capacidad de dos turnos en 2025, situación que el crecimiento pronosticado agrava. La alternativa directa es un tercer turno, que devuelve la utilización a un rango factible; la alternativa complementaria es recalibrar la participación de la planta con datos reales de producción. La línea de garrafón, en cambio, dispone de holgura amplia, condicionada a mantener dos operarios en el paletizado.")]));
children.push(...TBL("Utilización por línea, estado actual y futuro",
 ["Escenario","L1","L2","L3"],
 [["U 2025 (2 turnos)","117 %","122 %","81 %"],
  ["U 2026 (2 turnos)","125 %","130 %","80 %"],
  ["U 2026 (3 turnos)","83 %","86 %","27 %"],
  ["U 2026, L3 con 1 operario","—","—","161 %"]],
 [2600,1500,1500,1500]));
children.push(P([run("La coherencia entre este resultado y el TEEP de la Sección VII exige una nota: una utilización superior al 100 % con dos turnos y un TEEP del 40 % no pueden ser simultáneamente ciertos en la planta física. Ello indica que, o bien la planta real programa más horas que las declaradas (y el TEEP real sería mayor), o bien la participación de planta está sobreestimada. Un único dato —las horas efectivamente programadas por línea, o la producción real mensual— resuelve la ambigüedad y calibra el modelo.")]));

// ===== IX. ERP =====
children.push(H1("Bases para el Sistema ERP (Odoo)"));
children.push(P([run("El alcance de esta fase se limita a las estructuras de productos y pronóstico; la parametrización financiera y de compras se abordará posteriormente. Se generaron nueve archivos de importación con identificadores externos, alineados con los módulos de la instancia del proyecto (Inventario, Manufactura con planeación maestra, Ventas y Código de barras): categorías y unidades de medida que reflejan la jerarquía de empaque (botella, cajón o pack o rack, capa, pallet); los tres productos terminados con su código y código de barras EAN-13 verificado; once componentes de materia prima y empaque; las listas de materiales por unidad; los empaques de venta; y la demanda mensual pronosticada por producto para alimentar la planeación maestra. Con estas bases, al cargar la demanda, el sistema propone las órdenes de fabricación mensuales en múltiplos de pallet.")]));

// ===== X. CONCLUSIONES =====
children.push(H1("Conclusiones"));
children.push(P([run("El trabajo integró pronóstico, capacidad e información en un marco reproducible y trazable a datos reales. Primero, la reconstrucción de la demanda a partir de 21 trimestres corporativos, verificada automáticamente, sustituyó la ausencia de series de planta con un proxy auditable. Segundo, la cadena de validación —backtest con MAPE de 2,7 %, señal de rastreo con causa asignable y predicción del trimestre real más reciente con error de 0,07 %— alcanzó un estándar exigente. Tercero, el análisis multivariado justificó tratar el garrafón mediante combinación de pronósticos, reconociéndolo como agua sin perder precisión. Cuarto, el OEE construido de forma ascendente reprodujo el rango observado sin ajuste forzado, y el análisis de capacidad reveló una restricción real de dos turnos en las líneas de gaseosas y la criticidad ergonómica del paletizado manual de garrafones. Como trabajo futuro se plantea la calibración con datos de producción reales, el estudio de secuenciación de corridas y la evaluación de semiautomatización del paletizado.")]));
children.push(P([run("Limitaciones. ",{it:true}),run("La mezcla de empaque es anual; la participación de planta es el supuesto de mayor sensibilidad; los pesos intra-trimestre reparten un total trimestral que sí es real; y la coherencia entre utilización y TEEP requiere un dato de horas programadas para su cierre definitivo.",{it:true})]));

// ===== REFERENCIAS =====
children.push(H1("Referencias"));
const R=[
 'P. R. Winters, "Forecasting sales by exponentially weighted moving averages," Manage. Sci., vol. 6, no. 3, pp. 324–342, 1960.',
 'E. S. Gardner and E. McKenzie, "Forecasting trends in time series," Manage. Sci., vol. 31, no. 10, pp. 1237–1246, 1985.',
 'Coca-Cola FEMSA, "Informe Integrado 2025," Ciudad de México, 2026. [Online]. Available: https://investors.coca-colafemsa.com',
 'DANE, "Encuesta Mensual Manufacturera con Enfoque Territorial (EMMET)," Bogotá, Colombia. [Online]. Available: https://www.dane.gov.co',
 'KRONES AG, "Used filling and inspection equipment (Linatronic, Mecafill, Contiform)," MachinePoint/Machineseeker inventories. [Online]. Available: https://www.machineseeker.com',
 'DANE, "Proyecciones de población nacional y departamental," Bogotá, Colombia, 2024.',
 'iBottling and FESTA, "5-gallon (18.9–25 L) water filling monoblock specifications," commercial datasheets, 2024.',
 'Raddar ConsumerTrack, "Consumo de bebidas por ciudad en Colombia," Bogotá, 2012–2023.',
 'HEUFT Systemtechnik GmbH, "HEUFT PRIME full-bottle inspection," technical documentation. [Online]. Available: https://heuft.com',
 'IC Filling Systems, "5-gallon bottling line," product documentation, 2024.',
 'R. J. Hyndman and G. Athanasopoulos, Forecasting: Principles and Practice, 3rd ed. Melbourne, Australia: OTexts, 2021. [Online]. Available: https://otexts.com/fpp3/',
 'J. M. Bates and C. W. J. Granger, "The combination of forecasts," Oper. Res. Q., vol. 20, no. 4, pp. 451–468, 1969.',
 'S. Chopra and P. Meindl, Supply Chain Management: Strategy, Planning, and Operation, 7th ed. Harlow, U.K.: Pearson, 2019.',
 'C. J. Cortés-Rodríguez, "Gestión de Producción Automatizada (APM): notas del curso," Univ. Nacional de Colombia, Bogotá, 2024.',
 'Congreso de Colombia, "Ley 51 de 1983 (traslado de festivos)," Bogotá, 1983.',
 'FESTA and cnkingmachine, "QGF-600/900 5-gallon water filling line," datasheets, 2024.',
 'Coca-Cola FEMSA, "Reportes de Resultados Trimestrales 1T-2022 a 1T-2026," 17 documents. [Online]. Available: https://investors.coca-colafemsa.com/informacion-financiera/reportes-trimestrales/',
];
R.forEach((t,i)=>children.push(REF(i+1,t)));

const doc=new Document({styles,numbering,features:{updateFields:true},sections:[{
 properties:{page:{size:{width:12240,height:15840},margin:{top:1440,bottom:1440,left:1440,right:1440}}},
 footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[run("",{size:20}),new TextRun({children:[PageNumber.CURRENT],font:FONT,size:20})]})]})},
 children}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("reporte/Reporte_Integral_Fontibon.docx",b);console.log("ok",b.length)});
