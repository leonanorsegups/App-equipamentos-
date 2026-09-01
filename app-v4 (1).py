import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import json
import os
from datetime import datetime

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Orsegups - Simulador de Segurança PáP",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização geral para combinar com a identidade visual da Orsegups (Azul e Branco)
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
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #002d5a;
        color: #f0f0f0;
    }
    h1, h2, h3 {
        color: #004587;
    }
    .client-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #004587;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Função para obter o caminho do banco de dados (Garante que roda em qualquer lugar)
def get_db_path():
    if os.path.exists('/workspace/scratch'):
        return '/workspace/scratch/orsegups_leads.db'
    return 'orsegups_leads.db'

# Inicialização do Banco de Dados SQLite
def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT,
            cnpj TEXT,
            endereco TEXT,
            telefone TEXT,
            upfront_opcao TEXT,
            upfront_valor REAL,
            monitoramento_valor REAL,
            equipamentos TEXT,
            data_registro TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Funções de interação com o banco de dados
def salvar_cliente(nome, cpf, cnpj, endereco, telefone, upfront_opcao, upfront_valor, monitoramento_valor, equipamentos=""):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO leads (nome, cpf, cnpj, endereco, telefone, upfront_opcao, upfront_valor, monitoramento_valor, equipamentos, data_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cpf, cnpj, endereco, telefone, upfront_opcao, upfront_valor, monitoramento_valor, equipamentos, data_atual))
    conn.commit()
    conn.close()

def atualizar_cliente(lead_id, nome, cpf, cnpj, endereco, telefone, upfront_opcao, upfront_valor, monitoramento_valor):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        UPDATE leads 
        SET nome=?, cpf=?, cnpj=?, endereco=?, telefone=?, upfront_opcao=?, upfront_valor=?, monitoramento_valor=?
        WHERE id=?
    ''', (nome, cpf, cnpj, endereco, telefone, upfront_opcao, upfront_valor, monitoramento_valor, lead_id))
    conn.commit()
    conn.close()

def listar_clientes():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, nome, data_registro FROM leads ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def obter_cliente(lead_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
    row = c.fetchone()
    conn.close()
    return row

# Logotipo Orsegups e Título
st.image("https://www.orsegups.com.br/wp-content/uploads/2020/07/logo-orsegups.png", width=220)
st.title("Simulador de Ambientes Orsegups — Alarme 365")
st.markdown("""
**Ferramenta Integrada de Vendas Porta a Porta (PáP)**.
Insira as informações do cliente na barra lateral para habilitar e trabalhar no simulador de ambientes.
""")

# Barra Lateral (Sidebar) com cadastro unificado e banco de dados
with st.sidebar:
    st.header("📋 Cadastro do Cliente")
    
    # Busca por leads salvos
    clientes_salvos = listar_clientes()
    opcoes_clientes = ["-- Cadastrar Novo Cliente --"] + [f"{c[1]} ({c[2][:10]})" if (len(c) > 2 and c[2]) else c[1] for c in clientes_salvos]
    selecionado = st.selectbox("📂 Carregar Lead Salvo", opcoes_clientes)
    
    # Carrega dados do cliente se selecionado
    cliente_dados = None
    lead_id = None
    if selecionado != "-- Cadastrar Novo Cliente --":
        index_sel = opcoes_clientes.index(selecionado) - 1
        lead_id = clientes_salvos[index_sel][0]
        cliente_dados = obter_cliente(lead_id)

    st.markdown("---")
    
    # Campos de formulário
    nome = st.text_input("Nome Completo", value=cliente_dados[1] if cliente_dados else "", placeholder="Nome do Cliente")
    cpf = st.text_input("CPF (Opcional)", value=cliente_dados[2] if cliente_dados else "", placeholder="000.000.000-00")
    cnpj = st.text_input("CNPJ (Opcional)", value=cliente_dados[3] if cliente_dados else "", placeholder="00.000.000/0001-00")
    endereco = st.text_input("Endereço Completo", value=cliente_dados[4] if cliente_dados else "", placeholder="Rua, número, bairro")
    telefone = st.text_input("Telefone de Contato", value=cliente_dados[5] if cliente_dados else "", placeholder="(00) 90000-0000")
    
    st.markdown("### 💰 Condições Comerciais")
    upfront = st.radio("Cobrar Valor de Adesão/Upfront?", ["Não", "Sim"], index=1 if (cliente_dados and cliente_dados[6] == "Sim") else 0)
    
    valor_upfront = 0.0
    if upfront == "Sim":
        valor_upfront = st.number_input("Valor do Upfront (R$)", min_value=0.0, value=float(cliente_dados[7]) if (cliente_dados and cliente_dados[7]) else 199.0, step=50.0)
        
    valor_mensal = st.number_input("Valor do Monitoramento Mensal (R$)", min_value=0.0, value=float(cliente_dados[8]) if (cliente_dados and cliente_dados[8]) else 149.0, step=10.0)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botões inteligentes para salvar/atualizar
    if cliente_dados:
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Atualizar"):
                if nome:
                    atualizar_cliente(lead_id, nome, cpf, cnpj, endereco, telefone, upfront, valor_upfront, valor_mensal)
                    st.success("Dados atualizados!")
                    st.rerun()
                else:
                    st.error("Nome obrigatório!")
        with col_btn2:
            if st.button("➕ Novo Lead"):
                if nome:
                    salvar_cliente(nome, cpf, cnpj, endereco, telefone, upfront, valor_upfront, valor_mensal)
                    st.success("Novo lead cadastrado!")
                    st.rerun()
                else:
                    st.error("Nome obrigatório!")
    else:
        if st.button("💾 Salvar Cliente no Banco"):
            if nome:
                salvar_cliente(nome, cpf, cnpj, endereco, telefone, upfront, valor_upfront, valor_mensal)
                st.success(f"Lead de '{nome}' salvo!")
                st.rerun()
            else:
                st.error("Por favor, preencha o Nome Completo.")

# Verificação se o cadastro básico foi preenchido
if not nome:
    st.info("👈 **Aguardando Cadastro:** Preencha os dados do cliente e salve ou carregue um lead na barra lateral esquerda para destravar o simulador técnico.")
else:
    # Cabeçalho Informativo do Cliente Ativo
    st.markdown(f"""
    <div class="client-card">
        <h4>👤 Cliente Ativo: <strong>{nome}</strong></h4>
        <p style="margin:0; font-size:14px;">
            <strong>Telefone:</strong> {telefone or 'Não informado'} | 
            <strong>Endereço:</strong> {endereco or 'Não informado'} | 
            <strong>Mensalidade:</strong> R$ {valor_mensal:.2f} 
            {"| <strong>Taxa Upfront:</strong> R$ " + f"{valor_upfront:.2f}" if upfront == "Sim" else "| <strong>Taxa Upfront:</strong> Isento"}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # HTML/JS para o simulador
    canvas_html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <title>Simulador Orsegups</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f6f9;
                color: #333;
                overflow: hidden;
                touch-action: none;
            }}
            .container {{
                display: flex;
                flex-direction: row;
                gap: 15px;
                padding: 10px;
                height: 580px;
                box-sizing: border-box;
            }}
            .palette {{
                width: 260px;
                background: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                padding: 12px;
                display: flex;
                flex-direction: column;
                gap: 12px;
                overflow-y: auto;
            }}
            .palette h3 {{
                margin: 0 0 5px 0;
                color: #004587;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 5px;
                font-size: 14px;
            }}
            .tool-group {{
                display: flex;
                flex-direction: column;
                gap: 6px;
            }}
            .btn-tool {{
                padding: 8px 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background: #f8f9fa;
                cursor: pointer;
                font-weight: 600;
                text-align: left;
                font-size: 13px;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.2s;
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
                padding: 6px 8px;
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
                width: 28px;
                height: 28px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 15px;
                color: white;
                font-weight: bold;
            }}
            .bg-central {{ background-color: #004587; }}
            .bg-detector {{ background-color: #ff9900; }}
            .bg-sirene {{ background-color: #8b5cf6; }}
            .bg-magnetico {{ background-color: #10b981; }}
            .bg-controle {{ background-color: #ef4444; }}

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
            }}
            .canvas-header {{
                background: #004587;
                color: white;
                padding: 8px 12px;
                font-weight: bold;
                font-size: 13px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .canvas-header button {{
                background: rgba(255,255,255,0.2);
                border: none;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
                font-size: 11px;
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
                touch-action: none;
            }}
            .summary-box {{
                margin-top: auto;
                background: #f8f9fa;
                border-radius: 6px;
                padding: 8px;
                font-size: 12px;
                border: 1px solid #e9ecef;
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <!-- Paleta de ferramentas -->
        <div class="palette">
            <h3>✏️ Esboço Livre</h3>
            <div class="tool-group">
                <button class="btn-tool active" id="tool-wall" onclick="setTool('wall')">
                    <span>🧱</span> Desenho Livre (Paredes)
                </button>
                <button class="btn-tool" id="tool-erase" onclick="setTool('erase')">
                    <span>🧹</span> Borracha / Apagar
                </button>
                <button class="btn-tool" id="tool-select" onclick="setTool('select')">
                    <span>✋</span> Mover Dispositivo
                </button>
            </div>

            <h3>🚨 Equipamentos Orsegups</h3>
            <div class="tool-group">
                <div class="eq-item" onclick="setAddEquipment('detector')">
                    <div class="eq-icon bg-detector">📸</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Foto Detector</div>
                        <div style="font-size: 10px; color: #666;">Sensor de Imagem</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('central')">
                    <div class="eq-icon bg-central">P</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Painel Central</div>
                        <div style="font-size: 10px; color: #666;">Cérebro do Sistema</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('sirene')">
                    <div class="eq-icon bg-sirene">🔊</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Sirene</div>
                        <div style="font-size: 10px; color: #666;">Alerta Sonoro</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('magnetico')">
                    <div class="eq-icon bg-magnetico">🧲</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Magnético</div>
                        <div style="font-size: 10px; color: #666;">Sensor de Abertura</div>
                    </div>
                </div>
                <div class="eq-item" onclick="setAddEquipment('controle')">
                    <div class="eq-icon bg-controle">🔑</div>
                    <div>
                        <div style="font-weight: bold; font-size:12px;">Controle Remoto</div>
                        <div style="font-size: 10px; color: #666;">Ativação e Pânico SOS</div>
                    </div>
                </div>
            </div>

            <div class="summary-box">
                <div style="font-weight: bold; margin-bottom: 5px;">📦 Lista de Itens:</div>
                <div id="equipment-count">Nenhum item posicionado.</div>
            </div>
        </div>

        <!-- Área do Desenho -->
        <div class="canvas-area">
            <div class="canvas-header">
                <span>📐 Esboce o imóvel do cliente</span>
                <button onclick="clearCanvas()">Limpar Projeto</button>
            </div>
            <canvas id="canvas"></canvas>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        
        function resizeCanvas() {{
            const parent = canvas.parentElement;
            canvas.width = parent.clientWidth;
            canvas.height = parent.clientHeight - 35;
            drawAll();
        }}

        window.addEventListener('resize', resizeCanvas);
        setTimeout(resizeCanvas, 150);

        let currentTool = 'wall'; 
        let activeEquipmentType = null;
        let isDrawing = false;
        
        let paths = []; 
        let currentPath = [];
        let equipments = []; 
        let selectedEquipment = null;
        let isDragging = false;

        const eqConfig = {{
            central: {{ label: 'Painel Central', color: '#004587', text: 'P' }},
            detector: {{ label: 'Foto Detector', color: '#ff9900', text: '📸' }},
            sirene: {{ label: 'Sirene', color: '#8b5cf6', text: '🔊' }},
            magnetico: {{ label: 'Magnético', color: '#10b981', text: '🧲' }},
            controle: {{ label: 'Controle Remoto', color: '#ef4444', text: '🔑' }}
        }};

        function setTool(tool) {{
            currentTool = tool;
            activeEquipmentType = null;
            
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

        function stopAndGetPos(e) {{
            if (e.cancelable) e.preventDefault();
            const rect = canvas.getBoundingClientRect();
            if (e.touches && e.touches.length > 0) {{
                return {{
                    x: e.touches[0].clientX - rect.left,
                    y: e.touches[0].clientY - rect.top
                }};
            }}
            return {{
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            }};
        }}

        // Registro ativo para touch
        canvas.addEventListener('touchstart', (e) => {{
            const pos = stopAndGetPos(e);
            startInteraction(pos);
        }}, {{ passive: false }});

        canvas.addEventListener('touchmove', (e) => {{
            const pos = stopAndGetPos(e);
            moveInteraction(pos);
        }}, {{ passive: false }});

        canvas.addEventListener('touchend', (e) => {{
            if (e.cancelable) e.preventDefault();
            endInteraction();
        }}, {{ passive: false }});

        // Mouse events
        canvas.addEventListener('mousedown', (e) => {{
            const pos = stopAndGetPos(e);
            startInteraction(pos);
        }});

        canvas.addEventListener('mousemove', (e) => {{
            const pos = stopAndGetPos(e);
            moveInteraction(pos);
        }});

        canvas.addEventListener('mouseup', endInteraction);

        function startInteraction(pos) {{
            if (currentTool === 'wall') {{
                isDrawing = true;
                currentPath = [pos];
                paths.push(currentPath);
            }} else if (currentTool === 'erase') {{
                eraseAt(pos.x, pos.y);
            }} else if (currentTool === 'select') {{
                selectedEquipment = equipments.find(eq => {{
                    const dist = Math.hypot(eq.x - pos.x, eq.y - pos.y);
                    return dist < 22;
                }});
                if (selectedEquipment) {{
                    isDragging = true;
                }}
            }} else if (currentTool === 'add_eq' && activeEquipmentType) {{
                addEquipment(activeEquipmentType, pos.x, pos.y);
                setTool('select'); 
            }}
        }}

        function moveInteraction(pos) {{
            if (isDrawing && currentTool === 'wall') {{
                currentPath.push(pos);
                drawAll();
            }} else if (isDragging && selectedEquipment) {{
                selectedEquipment.x = pos.x;
                selectedEquipment.y = pos.y;
                drawAll();
            }}
        }}

        function endInteraction() {{
            isDrawing = false;
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
            paths = paths.filter(path => {{
                let keep = true;
                for (let pt of path) {{
                    if (Math.hypot(pt.x - x, pt.y - y) < 22) {{
                        keep = false;
                        break;
                    }}
                }}
                return keep;
            }});

            equipments = equipments.filter(eq => {{
                const dist = Math.hypot(eq.x - x, eq.y - y);
                return dist > 22;
            }});

            updateSummary();
            drawAll();
        }}

        function drawAll() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Grid background
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

            // Desenhar caminhos das paredes
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            paths.forEach(path => {{
                if (path.length < 2) return;
                ctx.beginPath();
                ctx.moveTo(path[0].x, path[0].y);
                for (let i = 1; i < path.length; i++) {{
                    ctx.lineTo(path[i].x, path[i].y);
                }}
                ctx.stroke();
            }});

            // Desenhar equipamentos
            equipments.forEach(eq => {{
                const config = eqConfig[eq.type];
                
                ctx.beginPath();
                ctx.arc(eq.x, eq.y, 16, 0, 2 * Math.PI);
                ctx.fillStyle = config.color;
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = '#ffffff';
                ctx.stroke();

                ctx.font = '14px Arial';
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
                container.innerHTML = "Nenhum item posicionado.";
                return;
            }}

            let html = '<ul style="margin: 0; padding-left: 15px; font-size:12px;">';
            for (const [type, count] of Object.entries(counts)) {{
                html += `<li><strong>${{count}}x</strong> ${{eqConfig[type].label}}</li>`;
            }}
            html += '</ul>';
            container.innerHTML = html;
        }}

        function clearCanvas() {{
            if(confirm("Deseja realmente limpar o esboço do imóvel?")) {{
                paths = [];
                equipments = [];
                updateSummary();
                drawAll();
            }}
        }}
    </script>
    </body>
    </html>
    """

    # Exibição do Canvas
    st.markdown("### 🗺️ Croqui e Distribuição de Dispositivos Orsegups")
    components.html(canvas_html, height=600, scrolling=False)

    # Conclusão e Resumo para Copiar
    st.markdown("---")
    st.subheader("📋 Resumo Comercial Formatado")

    upfront_texto = f"R$ {valor_upfront:.2f}" if upfront == "Sim" else "Grátis / Bonificado"

    resumo_texto = f"""🏢 PROPOSTA COMERCIAL ORSEGUPS — ALARME 365
--------------------------------------------------
👤 CLIENTE: {nome}
📞 TELEFONE: {telefone or 'Não cadastrado'}
📍 ENDEREÇO: {endereco or 'Não cadastrado'}
🪪 DOCUMENTO (CPF/CNPJ): {cpf or cnpj or 'Não informado'}

⭐ TECNOLOGIA PROPOSTA:
Instalação sem fios e sem obras com garantia vitalícia de equipamentos inclusa.

💰 VALORES DA PROPOSTA:
• Taxa de Adesão/Upfront: {upfront_texto}
• Monitoramento e Manutenção 24h: R$ {valor_mensal:.2f} / mensais

🛡️ Sua segurança ativa com a maior central de monitoramento do Brasil!
"""

    st.text_area("Copie o texto abaixo para enviar ao cliente:", resumo_texto, height=220)
