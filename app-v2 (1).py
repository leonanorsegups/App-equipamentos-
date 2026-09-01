import streamlit as st
import streamlit.components.v1 as components
import json

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Orsegups - Simulador de Vendas Porta a Porta (PáP)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização para combinar com a identidade visual da Orsegups
st.markdown("""
<style>
    .main {
        background-color: #f4f6f9;
    }
    .stButton>button {
        background-color: #004587;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #002d5a;
        color: #f0f0f0;
    }
    h1, h2, h3, h4 {
        color: #004587;
    }
    .client-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #004587;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Logo da Orsegups e cabeçalho principal
st.image("https://www.orsegups.com.br/wp-content/uploads/2020/07/logo-orsegups.png", width=220)
st.title("Simulador de Ambientes e Gerador de Propostas — Alarme 365")
st.markdown("""
**Plataforma Comercial de Vendas Porta a Porta (PáP).**
Cadastre o cliente, planeje a segurança desenhando uma planta livre em tempo real e simule o posicionamento estratégico dos sensores e dispositivos Orsegups.
""")

# Inicializar o estado do cadastro do cliente se não existir
if "cliente" not in st.session_state:
    st.session_state.cliente = {
        "registrado": False,
        "nome": "",
        "cpf": "",
        "cnpj": "",
        "endereco": "",
        "telefone": "",
        "upfront_opcao": "Não",
        "valor_upfront": 0.0,
        "valor_mensal": 149.0
    }

# Renderização condicional: Cadastro ou Área do Desenho
if not st.session_state.cliente["registrado"]:
    st.markdown("---")
    st.markdown("### 📋 Passo 1: Cadastrar Cliente e Parâmetros Comerciais")
    st.info("⚠️ O cadastro do cliente é obrigatório para liberar a área de desenho e posicionamento de equipamentos.")

    with st.form("cadastro_cliente_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo do Cliente *", placeholder="Ex: João da Silva", value=st.session_state.cliente["nome"])
            cpf = st.text_input("CPF (Pessoa Física)", placeholder="000.000.000-00", value=st.session_state.cliente["cpf"])
            telefone = st.text_input("Telefone / WhatsApp *", placeholder="(00) 90000-0000", value=st.session_state.cliente["telefone"])
        with col2:
            endereco = st.text_input("Endereço Completo (Local da Instalação) *", placeholder="Rua, Número, Bairro, Cidade - UF", value=st.session_state.cliente["endereco"])
            cnpj = st.text_input("CNPJ (Pessoa Jurídica)", placeholder="00.000.000/0000-00", value=st.session_state.cliente["cnpj"])
            
        st.markdown("#### 💰 Configuração Comercial")
        c1, c2 = st.columns(2)
        with c1:
            upfront_opt = st.selectbox("Possui Valor de Adesão/Instalação (Upfront)?", ["Não", "Sim"], index=0 if st.session_state.cliente["upfront_opcao"] == "Não" else 1)
            
            # Campo condicional para valor do upfront
            valor_upfront_input = 0.0
            if upfront_opt == "Sim":
                valor_upfront_input = st.number_input(
                    "Valor do Upfront (R$)", 
                    min_value=0.0, 
                    value=st.session_state.cliente["valor_upfront"] if st.session_state.cliente["valor_upfront"] > 0 else 199.0, 
                    step=50.0
                )
        with c2:
            valor_mensal_input = st.number_input("Valor do Monitoramento Mensal (R$/mês)", min_value=0.0, value=st.session_state.cliente["valor_mensal"], step=10.0)

        st.markdown("<br>", unsafe_allow_html=True)
        salvar = st.form_submit_state = st.form_submit_button("Salvar Cadastro e Liberar Simulador")
        
        if salvar:
            if not nome or not endereco or not telefone:
                st.error("Por favor, preencha todos os campos obrigatórios (*).")
            else:
                st.session_state.cliente["registrado"] = True
                st.session_state.cliente["nome"] = nome
                st.session_state.cliente["cpf"] = cpf
                st.session_state.cliente["cnpj"] = cnpj
                st.session_state.cliente["endereco"] = endereco
                st.session_state.cliente["telefone"] = telefone
                st.session_state.cliente["upfront_opcao"] = upfront_opt
                st.session_state.cliente["valor_upfront"] = valor_upfront_input if upfront_opt == "Sim" else 0.0
                st.session_state.cliente["valor_mensal"] = valor_mensal_input
                st.success("Cadastro salvo com sucesso! Redirecionando para a área de simulação...")
                st.rerun()

else:
    # CLIENTE CADASTRADO: Exibir tela do simulador
    
    # Barra Lateral para visualização e edição rápida do cadastro
    with st.sidebar:
        st.markdown("### 👤 Cliente Selecionado")
        st.markdown(f"""
        **Nome:** {st.session_state.cliente['nome']}
        **Telefone:** {st.session_state.cliente['telefone']}
        **Endereço:** {st.session_state.cliente['endereco']}
        """)
        if st.session_state.cliente['cpf']:
            st.markdown(f"**CPF:** {st.session_state.cliente['cpf']}")
        if st.session_state.cliente['cnpj']:
            st.markdown(f"**CNPJ:** {st.session_state.cliente['cnpj']}")
            
        st.markdown("---")
        st.markdown("### 💰 Condições Financeiras")
        if st.session_state.cliente['upfront_opcao'] == "Sim":
            st.markdown(f"**Taxa de Instalação (Upfront):** R$ {st.session_state.cliente['valor_upfront']:.2f}")
        else:
            st.markdown("**Taxa de Instalação (Upfront):** Grátis / Isento")
        st.markdown(f"**Mensalidade de Monitoramento:** R$ {st.session_state.cliente['valor_mensal']:.2f}/mês")
        
        st.markdown("---")
        if st.button("✏️ Editar Cadastro / Mudar Valores"):
            st.session_state.cliente["registrado"] = False
            st.rerun()

    # Passar os dados do cliente para o HTML/JS como JSON
    cliente_json = json.dumps(st.session_state.cliente, ensure_ascii=False)

    # Componente HTML/Canvas customizado para desenho livre e posicionamento de equipamentos
    canvas_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Simulador Orsegups</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f6f9;
                color: #333;
                overflow: hidden; /* Impede rolagem na página inteira no Streamlit iframe */
            }}
            .container {{
                display: flex;
                flex-direction: row;
                gap: 15px;
                padding: 10px;
                height: calc(100vh - 20px);
                box-sizing: border-box;
            }}
            @media (max-width: 900px) {{
                .container {{
                    flex-direction: column;
                    height: auto;
                    overflow-y: auto;
                }}
                .canvas-area {{
                    height: 450px !important;
                }}
                .palette {{
                    width: 100% !important;
                }}
            }}
            /* Paleta lateral esquerda */
            .palette {{
                width: 280px;
                background: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                padding: 15px;
                display: flex;
                flex-direction: column;
                gap: 12px;
                box-sizing: border-box;
                flex-shrink: 0;
            }}
            .palette h3 {{
                margin: 0;
                color: #004587;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 5px;
                font-size: 15px;
            }}
            .tool-group {{
                display: flex;
                flex-direction: column;
                gap: 6px;
            }}
            .btn-tool {{
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background: #f8f9fa;
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
                text-align: left;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .btn-tool:hover {{
                background: #e9ecef;
                border-color: #004587;
            }}
            .btn-tool.active {{
                background: #004587;
                color: white;
                border-color: #004587;
            }}
            .eq-item {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 8px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background: #ffffff;
                cursor: pointer;
                user-select: none;
                transition: transform 0.1s;
            }}
            .eq-item:hover {{
                transform: scale(1.02);
                border-color: #004587;
            }}
            .eq-icon {{
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
                color: white;
                font-weight: bold;
                flex-shrink: 0;
            }}
            /* Cores dos Equipamentos */
            .bg-foto {{ background-color: #ff9900; }}    /* Laranja */
            .bg-central {{ background-color: #004587; }} /* Azul Orsegups */
            .bg-sirene {{ background-color: #8b5cf6; }}  /* Roxo */
            .bg-magnetico {{ background-color: #10b981; }}/* Verde */
            .bg-controle {{ background-color: #ef4444; }} /* Vermelho */

            /* Área de Desenho */
            .canvas-area {{
                flex-grow: 1;
                background: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                border: 2px dashed #004587;
                box-sizing: border-box;
            }}
            .canvas-header {{
                background: #004587;
                color: white;
                padding: 10px 15px;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 14px;
            }}
            .canvas-header button {{
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                font-size: 12px;
            }}
            .canvas-header button:hover {{
                background: rgba(255,255,255,0.4);
            }}
            #canvas {{
                flex-grow: 1;
                width: 100%;
                height: 100%;
                background-color: #fafafa;
                background-image: radial-gradient(#e0e0e0 1px, transparent 1px);
                background-size: 20px 20px;
                cursor: crosshair;
                touch-action: none; /* ESSENCIAL para bloquear a rolagem por toque no celular */
                user-select: none;
                -webkit-user-select: none;
            }}
            /* Listagem de itens inseridos */
            .summary-box {{
                margin-top: auto;
                background: #f8f9fa;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
                border: 1px solid #e9ecef;
            }}
            .btn-copy {{
                margin-top: 8px;
                background: #10b981;
                color: white;
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
                cursor: pointer;
                text-align: center;
                font-size: 12px;
                transition: background 0.2s;
            }}
            .btn-copy:hover {{
                background: #059669;
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <!-- Painel de Controle Esquerdo -->
        <div class="palette">
            <h3>✏️ Ferramentas</h3>
            <div class="tool-group">
                <button class="btn-tool active" id="tool-wall" onclick="setTool('wall')">
                    <span>🖌️</span> Desenhar Planta Livre
                </button>
                <button class="btn-tool" id="tool-erase" onclick="setTool('erase')">
                    <span>🧹</span> Borracha (Linha/Equip)
                </button>
                <button class="btn-tool" id="tool-select" onclick="setTool('select')">
                    <span>✋</span> Mover Equipamentos
                </button>
            </div>

            <h3>🚨 Equipamentos do Projeto</h3>
            <div class="tool-group">
                <div class="eq-item" onclick="setAddEquipment('foto_detector')">
                    <div class="eq-icon bg-foto">📸</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Foto Detector</div>
                        <div style="font-size: 10px; color: #666;">Verificação por imagem</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('painel_central')">
                    <div class="eq-icon bg-central">🏠</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Painel Central</div>
                        <div style="font-size: 10px; color: #666;">Cérebro do Alarme 365</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('sirene')">
                    <div class="eq-icon bg-sirene">🔊</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Sirene</div>
                        <div style="font-size: 10px; color: #666;">Alerta sonoro potente</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('magnetico')">
                    <div class="eq-icon bg-magnetico">🧲</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Magnético</div>
                        <div style="font-size: 10px; color: #666;">Sensores de portas/janelas</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('controle_remoto')">
                    <div class="eq-icon bg-controle">🔑</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Controle Remoto</div>
                        <div style="font-size: 10px; color: #666;">Ativação e botão de SOS</div>
                    </div>
                </div>
            </div>

            <div class="summary-box">
                <div style="font-weight: bold; margin-bottom: 5px; color: #004587;">📦 Lista de Equipamentos:</div>
                <div id="equipment-count">Nenhum equipamento inserido ainda.</div>
                <button class="btn-copy" onclick="copyFullProposal()">📋 Copiar Proposta Completa</button>
            </div>
        </div>

        <!-- Área da Planta Baixa -->
        <div class="canvas-area">
            <div class="canvas-header">
                <span id="canvas-title">📐 Esboço de Segurança Orsegups</span>
                <button onclick="clearCanvas()">Limpar Projeto</button>
            </div>
            <canvas id="canvas"></canvas>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        // Dados do cliente passados dinamicamente pelo Streamlit
        const cliente = {cliente_json};

        // Atualiza cabeçalho com nome do cliente
        document.getElementById('canvas-title').innerText = "📐 Esboço para: " + cliente.nome;

        // Configuração do tamanho do Canvas
        function resizeCanvas() {{
            const parent = canvas.parentElement;
            canvas.width = parent.clientWidth;
            canvas.height = parent.clientHeight - 40; // Desconta cabeçalho
            drawAll();
        }}

        window.addEventListener('resize', resizeCanvas);
        setTimeout(resizeCanvas, 150);

        // Bloquear totalmente a rolagem e o comportamento de puxar para atualizar (iOS/Android)
        function preventBehavior(e) {{
            if (e.target === canvas) {{
                e.preventDefault();
            }}
        }}
        document.body.addEventListener('touchstart', preventBehavior, {{ passive: false }});
        document.body.addEventListener('touchmove', preventBehavior, {{ passive: false }});
        document.body.addEventListener('touchend', preventBehavior, {{ passive: false }});

        // Estados e variáveis globais
        let currentTool = 'wall'; // wall, erase, select, add_eq
        let activeEquipmentType = null;
        let isDrawing = false;
        
        let strokes = []; // Array de traços libres: [ [{{x, y}}, {{x, y}}, ...] ]
        let currentStroke = [];
        
        let equipments = []; // [{{id, type, x, y}}]
        let selectedEquipment = null;
        let isDragging = false;

        // Dicionário de Equipamentos em Português
        const eqConfig = {{
            foto_detector: {{ label: 'Foto Detector', color: '#ff9900', text: '📸' }},
            painel_central: {{ label: 'Painel Central', color: '#004587', text: '🏠' }},
            sirene: {{ label: 'Sirene', color: '#8b5cf6', text: '🔊' }},
            magnetico: {{ label: 'Magnético', color: '#10b981', text: '🧲' }},
            controle_remoto: {{ label: 'Controle Remoto', color: '#ef4444', text: '🔑' }}
        }};

        function setTool(tool) {{
            currentTool = tool;
            activeEquipmentType = null;
            
            // Alterar classes ativas na paleta
            document.querySelectorAll('.btn-tool').forEach(b => b.classList.remove('active'));
            document.getElementById('tool-' + tool).classList.add('active');
            
            if (tool === 'select') {{
                canvas.style.cursor = 'move';
            }} else if (tool === 'erase') {{
                canvas.style.cursor = 'cell';
            }} else {{
                canvas.style.cursor = 'crosshair';
            }}
        }}

        function setAddEquipment(type) {{
            currentTool = 'add_eq';
            activeEquipmentType = type;
            document.querySelectorAll('.btn-tool').forEach(b => b.classList.remove('active'));
            canvas.style.cursor = 'pointer';
        }}

        // Captura de posições unificada (Mouse e Touch)
        function getMousePos(e) {{
            const rect = canvas.getBoundingClientRect();
            let clientX, clientY;
            
            if (e.touches && e.touches.length > 0) {{
                clientX = e.touches[0].clientX;
                clientY = e.touches[0].clientY;
            }} else {{
                clientX = e.clientX;
                clientY = e.clientY;
            }}
            
            return {{
                x: clientX - rect.left,
                y: clientY - rect.top
            }};
        }}

        // Manipulação de Eventos
        canvas.addEventListener('mousedown', startInteraction);
        canvas.addEventListener('mousemove', moveInteraction);
        canvas.addEventListener('mouseup', endInteraction);

        canvas.addEventListener('touchstart', function(e) {{
            e.preventDefault();
            startInteraction(e);
        }}, {{ passive: false }});

        canvas.addEventListener('touchmove', function(e) {{
            e.preventDefault();
            moveInteraction(e);
        }}, {{ passive: false }});

        canvas.addEventListener('touchend', function(e) {{
            e.preventDefault();
            endInteraction(e);
        }}, {{ passive: false }});

        function startInteraction(e) {{
            const pos = getMousePos(e);

            if (currentTool === 'wall') {{
                isDrawing = true;
                currentStroke = [pos];
            }} else if (currentTool === 'erase') {{
                eraseAt(pos.x, pos.y);
            }} else if (currentTool === 'select') {{
                selectedEquipment = equipments.find(eq => {{
                    return Math.hypot(eq.x - pos.x, eq.y - pos.y) < 22;
                }});
                if (selectedEquipment) {{
                    isDragging = true;
                }}
            }} else if (currentTool === 'add_eq' && activeEquipmentType) {{
                addEquipment(activeEquipmentType, pos.x, pos.y);
                setTool('select');
            }}
        }}

        function moveInteraction(e) {{
            const pos = getMousePos(e);

            if (isDrawing && currentTool === 'wall') {{
                currentStroke.push(pos);
                drawAll();
                
                // Desenha a linha atual de preview
                ctx.beginPath();
                ctx.strokeStyle = '#1e293b';
                ctx.lineWidth = 4;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.moveTo(currentStroke[0].x, currentStroke[0].y);
                for (let i = 1; i < currentStroke.length; i++) {{
                    ctx.lineTo(currentStroke[i].x, currentStroke[i].y);
                }}
                ctx.stroke();
            }} else if (isDragging && selectedEquipment) {{
                selectedEquipment.x = pos.x;
                selectedEquipment.y = pos.y;
                drawAll();
            }}
        }}

        function endInteraction(e) {{
            if (isDrawing && currentTool === 'wall') {{
                if (currentStroke.length > 1) {{
                    strokes.push(currentStroke);
                }}
                isDrawing = false;
                currentStroke = [];
                drawAll();
            }}
            isDragging = false;
            selectedEquipment = null;
        }}

        function addEquipment(type, x, y) {{
            equipments.push({{
                id: Date.now() + Math.random().toString(36).substr(2, 5),
                type: type,
                x: x,
                y: y
            }});
            updateSummary();
            drawAll();
        }}

        function eraseAt(x, y) {{
            // Remove traços que passam perto da borracha
            strokes = strokes.filter(stroke => {{
                const isClose = stroke.some(p => Math.hypot(p.x - x, p.y - y) < 15);
                return !isClose;
            }});

            // Remove equipamentos
            equipments = equipments.filter(eq => {{
                return Math.hypot(eq.x - x, eq.y - y) > 20;
            }});

            updateSummary();
            drawAll();
        }}

        function drawAll() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Desenhar Grid Quadriculado
            ctx.beginPath();
            ctx.strokeStyle = '#f1f1f1';
            ctx.lineWidth = 1;
            for (let x = 0; x < canvas.width; x += 20) {{
                ctx.moveTo(x, 0);
                ctx.lineTo(x, canvas.height);
            }}
            for (let y = 0; y < canvas.height; y += 20) {{
                ctx.moveTo(0, y);
                ctx.lineTo(canvas.width, y);
            }}
            ctx.stroke();

            // Desenhar Linhas Livres (Planta Baixa)
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            strokes.forEach(stroke => {{
                if (stroke.length < 1) return;
                ctx.beginPath();
                ctx.moveTo(stroke[0].x, stroke[0].y);
                for (let i = 1; i < stroke.length; i++) {{
                    ctx.lineTo(stroke[i].x, stroke[i].y);
                }}
                ctx.stroke();
            }});

            // Desenhar Equipamentos
            equipments.forEach(eq => {{
                const config = eqConfig[eq.type];
                
                // Círculo principal
                ctx.beginPath();
                ctx.arc(eq.x, eq.y, 16, 0, 2 * Math.PI);
                ctx.fillStyle = config.color;
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = '#ffffff';
                ctx.stroke();

                // Desenhar Ícone
                ctx.font = '14px sans-serif';
                ctx.fillStyle = '#ffffff';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(config.text, eq.x, eq.y);
            }});
        }}

        function updateSummary() {{
            const counts = {{}};
            equipments.forEach(eq => {{
                counts[eq.type] = (counts[eq.type] || 0) + 1;
            }});

            const container = document.getElementById('equipment-count');
            if (equipments.length === 0) {{
                container.innerHTML = "Nenhum equipamento inserido ainda.";
                return;
            }}

            let html = '<ul style="margin: 0; padding-left: 15px; font-size:11px; line-height: 1.4;">';
            for (const [type, count] of Object.entries(counts)) {{
                html += `<li><strong>${{count}}x</strong> ${{eqConfig[type].label}}</li>`;
            }}
            html += '</ul>';
            container.innerHTML = html;
        }}

        function clearCanvas() {{
            if (confirm("Deseja realmente limpar o esboço e começar de novo?")) {{
                strokes = [];
                equipments = [];
                updateSummary();
                drawAll();
            }}
        }}

        // Função para compilar e copiar a proposta completa para a área de transferência
        function copyFullProposal() {{
            const counts = {{}};
            equipments.forEach(eq => {{
                counts[eq.type] = (counts[eq.type] || 0) + 1;
            }});

            let eqListText = "";
            for (const [type, count] of Object.entries(counts)) {{
                eqListText += `- ${{count}}x ${{eqConfig[type].label}}\\n`;
            }}
            if (eqListText === "") eqListText = "- Nenhum equipamento selecionado no desenho.\\n";

            const upfrontText = cliente.upfront_opcao === "Sim" 
                ? `R$ ${{parseFloat(cliente.valor_upfront).toFixed(2)}}` 
                : "Grátis / Isento";

            const proposalText = 
`PROPOSTA COMERCIAL PERSONALIZADA — ORSEGUPS
--------------------------------------------------
CLIENTE: ${{cliente.nome}}
TELEFONE: ${{cliente.telefone}}
ENDEREÇO: ${{cliente.endereco}}
${{cliente.cpf ? 'CPF: ' + cliente.cpf + '\\n' : ''}}${{cliente.cnpj ? 'CNPJ: ' + cliente.cnpj + '\\n' : ''}}
--------------------------------------------------
EQUIPAMENTOS PREVISTOS NO PROJETO:
${{eqListText}}
--------------------------------------------------
CONDIÇÕES FINANCEIRAS:
• Taxa de Instalação (Upfront): ${{upfrontText}}
• Monitoramento 24h: R$ ${{parseFloat(cliente.valor_mensal).toFixed(2)}}/mês

Diferenciais Inclusos:
- Instalação imediata sem fio e sem reformas.
- Verificação instantânea de ocorrências por Imagem.
- Sistema inteligente Fala e Escuta integrado.
- Central conectada 24h com a maior e mais moderna central do Brasil.
- Garantia Vitalícia nos equipamentos enquanto mantido o monitoramento.
--------------------------------------------------`;

            navigator.clipboard.writeText(proposalText).then(() => {{
                alert("Proposta Comercial copiada com sucesso para a Área de Transferência!");
            }}).catch(err => {{
                console.error("Erro ao copiar proposta: ", err);
                alert("Não foi possível copiar automaticamente. Selecione e copie o texto manualmente.");
            }});
        }}
    </script>

    </body>
    </html>
    """

    st.markdown("### 🗺️ Área de Desenho Livre e Planejamento Técnico")
    
    # Renderiza o HTML canvas, passando o JSON do cliente incorporado
    components.html(canvas_html.replace("{cliente_json}", cliente_json), height=600, scrolling=False)
    
    # Exibição resumida dos dados comerciais para confirmação visual rápida
    st.markdown("---")
    st.markdown("### 🔍 Resumo de Condições Contratuais")
    colA, colB, colC = st.columns(3)
    with colA:
        st.markdown(f"**Cliente:** {st.session_state.cliente['nome']}")
    with colB:
        up_valor = f"R$ {st.session_state.cliente['valor_upfront']:.2f}" if st.session_state.cliente['upfront_opcao'] == "Sim" else "Isento"
        st.markdown(f"**Taxa Adesão/Upfront:** {up_valor}")
    with colC:
        st.markdown(f"**Monitoramento Mensal:** R$ {st.session_state.cliente['valor_mensal']:.2f}/mês")
