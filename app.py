import streamlit as st
import streamlit.components.v1 as components

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
    }
    .stButton>button:hover {
        background-color: #002d5a;
        color: #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #004587;
    }
    .highlight-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #004587;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da aplicação
st.image("https://www.orsegups.com.br/wp-content/uploads/2020/07/logo-orsegups.png", width=250)
st.title("Simulador Interativo de Ambientes — Alarme 365 Orsegups")
st.markdown("""
**Ferramenta de Apoio para Vendas Porta a Porta (PáP).** 
Desenhe o esboço da residência ou comércio do seu cliente e distribua estrategicamente os sensores e dispositivos do sistema **Alarme 365** para apresentar uma proposta visual de impacto!
""")

# Sidebar com informações do cliente e seletor de proposta
with st.sidebar:
    st.header("📋 Dados do Cliente")
    nome_cliente = st.text_input("Nome do Cliente", placeholder="Ex: João Silva")
    tipo_imovel = st.selectbox("Tipo de Imóvel", ["Residencial", "Comercial"])
    
    st.markdown("---")
    st.header("🔒 Diferenciais Alarme 365")
    st.markdown("""
    *   **Instalação Imediata** sem fios e sem obras.
    *   **Verificação por imagem** sem falsos alarmes.
    *   **Sistema Fala e Escuta** em tempo real.
    *   **Função SOS** de pânico silencioso.
    *   **Garantia Vitalícia** de equipamentos.
    *   Suporte da **maior central de monitoramento do país**.
    """)
    
    st.markdown("---")
    st.info("💡 **Dica de Venda:** Desenhe o contorno básico das paredes, posicione a Central no ponto mais protegido e coloque os sensores com câmera cobrindo os acessos principais.")

# Componente HTML/JS Interativo para o Desenho e Posicionamento de Equipamentos
# Este código roda inteiramente no navegador do cliente (perfeito para uso em campo sem lags)
canvas_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulador Orsegups</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f6f9;
            color: #333;
        }
        .container {
            display: flex;
            flex-direction: row;
            gap: 20px;
            padding: 10px;
            height: calc(100vh - 40px);
        }
        @media (max-width: 900px) {
            .container {
                flex-direction: column;
                height: auto;
            }
            .canvas-area {
                width: 100% !important;
                height: 500px !important;
            }
            .palette {
                width: 100% !important;
            }
        }
        /* Paleta de Ferramentas */
        .palette {
            width: 250px;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .palette h3 {
            margin-top: 0;
            color: #004587;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 8px;
            font-size: 16px;
        }
        .tool-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .btn-tool {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
            background: #f8f9fa;
            cursor: pointer;
            font-weight: 600;
            text-align: left;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .btn-tool:hover {
            background: #e9ecef;
            border-color: #004587;
        }
        .btn-tool.active {
            background: #004587;
            color: white;
            border-color: #004587;
        }
        .eq-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            background: #ffffff;
            cursor: grab;
            user-select: none;
            transition: transform 0.1s;
        }
        .eq-item:hover {
            transform: scale(1.02);
            border-color: #004587;
        }
        .eq-icon {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: white;
            font-weight: bold;
        }
        /* Cores dos Equipamentos */
        .bg-central { background-color: #004587; } /* Azul escuro */
        .bg-camera { background-color: #ff9900; }  /* Laranja */
        .bg-teclado { background-color: #10b981; } /* Verde */
        .bg-sos { background-color: #ef4444; }     /* Vermelho */
        .bg-sirene { background-color: #8b5cf6; }  /* Roxo */

        /* Área de Desenho */
        .canvas-area {
            flex-grow: 1;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            border: 2px dashed #004587;
        }
        .canvas-header {
            background: #004587;
            color: white;
            padding: 10px 15px;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .canvas-header button {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        .canvas-header button:hover {
            background: rgba(255,255,255,0.4);
        }
        #canvas {
            flex-grow: 1;
            width: 100%;
            height: 100%;
            background-color: #fafafa;
            background-image: radial-gradient(#e0e0e0 1px, transparent 1px);
            background-size: 20px 20px;
            cursor: crosshair;
        }
        /* Listagem de itens inseridos */
        .summary-box {
            margin-top: auto;
            background: #f8f9fa;
            border-radius: 6px;
            padding: 10px;
            font-size: 13px;
            border: 1px solid #e9ecef;
        }
    </style>
</head>
<body>

<div class="container">
    <!-- Painel de Controle Esquerdo -->
    <div class="palette">
        <h3>✏️ Modo de Desenho</h3>
        <div class="tool-group">
            <button class="btn-tool active" id="tool-wall" onclick="setTool('wall')">
                <span>🧱</span> Desenhar Paredes
            </button>
            <button class="btn-tool" id="tool-erase" onclick="setTool('erase')">
                <span>🧹</span> Borracha de Paredes
            </button>
            <button class="btn-tool" id="tool-select" onclick="setTool('select')">
                <span>✋</span> Mover Equipamentos
            </button>
        </div>

        <h3>🚨 Adicionar Equipamento Orsegups</h3>
        <div class="tool-group">
            <div class="eq-item" onclick="setAddEquipment('central')">
                <div class="eq-icon bg-central">C</div>
                <div>
                    <div style="font-weight: bold; font-size:13px;">Central Alarme 365</div>
                    <div style="font-size: 11px; color: #666;">Cérebro sem fio</div>
                </div>
            </div>
            <div class="eq-item" onclick="setAddEquipment('camera')">
                <div class="eq-icon bg-camera">📸</div>
                <div>
                    <div style="font-weight: bold; font-size:13px;">Sensor com Câmera</div>
                    <div style="font-size: 11px; color: #666;">Verificação por imagem</div>
                </div>
            </div>
            <div class="eq-item" onclick="setAddEquipment('teclado')">
                <div class="eq-icon bg-teclado">💬</div>
                <div>
                    <div style="font-weight: bold; font-size:13px;">Painel Fala/Escuta</div>
                    <div style="font-size: 11px; color: #666;">Interativo por áudio</div>
                </div>
            </div>
            <div class="eq-item" onclick="setAddEquipment('sos')">
                <div class="eq-icon bg-sos">🆘</div>
                <div>
                    <div style="font-weight: bold; font-size:13px;">Botão de Pânico SOS</div>
                    <div style="font-size: 11px; color: #666;">Disparo de pânico rápido</div>
                </div>
            </div>
            <div class="eq-item" onclick="setAddEquipment('sirene')">
                <div class="eq-icon bg-sirene">🔊</div>
                <div>
                    <div style="font-weight: bold; font-size:13px;">Sirene Externa</div>
                    <div style="font-size: 11px; color: #666;">Alerta sonoro potente</div>
                </div>
            </div>
        </div>

        <div class="summary-box">
            <div style="font-weight: bold; margin-bottom: 5px;">📦 Lista de Equipamentos:</div>
            <div id="equipment-count">Nenhum equipamento inserido ainda.</div>
        </div>
    </div>

    <!-- Área da Planta Baixa -->
    <div class="canvas-area">
        <div class="canvas-header">
            <span>📐 Planta Baixa e Projeto de Segurança</span>
            <button onclick="clearCanvas()">Limpar Projeto</button>
        </div>
        <canvas id="canvas"></canvas>
    </div>
</div>

<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    
    // Configurar o tamanho adequado do canvas
    function resizeCanvas() {
        const parent = canvas.parentElement;
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight - 40; // desconta cabeçalho
        drawAll();
    }

    window.addEventListener('resize', resizeCanvas);
    setTimeout(resizeCanvas, 100);

    // Estados e variáveis globais
    let currentTool = 'wall'; // wall, erase, select, add_eq
    let activeEquipmentType = null;
    let isDrawing = false;
    let startX, startY;
    
    let walls = []; // [{x1, y1, x2, y2}]
    let equipments = []; // [{id, type, x, y, size: 20}]
    let selectedEquipment = null;
    let isDragging = false;

    // Equipamentos predefinidos com estilo
    const eqConfig = {
        central: { label: 'Central', color: '#004587', text: 'C' },
        camera: { label: 'Sensor Câmera', color: '#ff9900', text: '📸' },
        teclado: { label: 'Fala e Escuta', color: '#10b981', text: '💬' },
        sos: { label: 'Botão SOS', color: '#ef4444', text: '🆘' },
        sirene: { label: 'Sirene', color: '#8b5cf6', text: '🔊' }
    };

    function setTool(tool) {
        currentTool = tool;
        activeEquipmentType = null;
        
        // Atualizar estado ativo nos botões
        document.querySelectorAll('.btn-tool').forEach(b => b.classList.remove('active'));
        document.getElementById('tool-' + tool).classList.add('active');
        
        if (tool === 'select') {
            canvas.style.cursor = 'move';
        } else if (tool === 'erase') {
            canvas.style.cursor = 'cell';
        } else {
            canvas.style.cursor = 'crosshair';
        }
    }

    function setAddEquipment(type) {
        currentTool = 'add_eq';
        activeEquipmentType = type;
        document.querySelectorAll('.btn-tool').forEach(b => b.classList.remove('active'));
        canvas.style.cursor = 'pointer';
    }

    // Interações com o mouse e toque (compatibilidade com tablets)
    canvas.addEventListener('mousedown', startInteraction);
    canvas.addEventListener('mousemove', moveInteraction);
    canvas.addEventListener('mouseup', endInteraction);

    canvas.addEventListener('touchstart', (e) => {
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent("mousedown", {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    });

    canvas.addEventListener('touchmove', (e) => {
        const touch = e.touches[0];
        const mouseEvent = new MouseEvent("mousemove", {
            clientX: touch.clientX,
            clientY: touch.clientY
        });
        canvas.dispatchEvent(mouseEvent);
    });

    canvas.addEventListener('touchend', () => {
        const mouseEvent = new MouseEvent("mouseup", {});
        canvas.dispatchEvent(mouseEvent);
    });

    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    function startInteraction(e) {
        const pos = getMousePos(e);
        startX = pos.x;
        startY = pos.y;

        if (currentTool === 'wall') {
            isDrawing = true;
        } else if (currentTool === 'erase') {
            eraseAt(pos.x, pos.y);
        } else if (currentTool === 'select') {
            // Verificar se clicou em algum equipamento
            selectedEquipment = equipments.find(eq => {
                const dist = Math.hypot(eq.x - pos.x, eq.y - pos.y);
                return dist < 20;
            });
            if (selectedEquipment) {
                isDragging = true;
            }
        } else if (currentTool === 'add_eq' && activeEquipmentType) {
            addEquipment(activeEquipmentType, pos.x, pos.y);
            setTool('select'); // Volta automaticamente para mover para fácil ajuste
        }
    }

    function moveInteraction(e) {
        const pos = getMousePos(e);

        if (isDrawing && currentTool === 'wall') {
            drawAll();
            // Desenhar linha de preview temporária
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(pos.x, pos.y);
            ctx.strokeStyle = '#004587';
            ctx.lineWidth = 4;
            ctx.lineCap = 'round';
            ctx.stroke();
        } else if (isDragging && selectedEquipment) {
            selectedEquipment.x = pos.x;
            selectedEquipment.y = pos.y;
            drawAll();
        }
    }

    function endInteraction(e) {
        if (isDrawing && currentTool === 'wall') {
            const pos = getMousePos(e);
            // Só adiciona se tiver um tamanho mínimo (evita pontos acidentais)
            if (Math.hypot(pos.x - startX, pos.y - startY) > 10) {
                walls.push({ x1: startX, y1: startY, x2: pos.x, y2: pos.y });
            }
            isDrawing = false;
            drawAll();
        }
        isDragging = false;
        selectedEquipment = null;
    }

    function addEquipment(type, x, y) {
        equipments.push({
            id: Date.now() + Math.random().toString(36).substr(2, 5),
            type: type,
            x: x,
            y: y
        });
        updateSummary();
        drawAll();
    }

    function eraseAt(x, y) {
        // Remove paredes próximas ao clique da borracha
        walls = walls.filter(wall => {
            // Distância simples ponto-segmento
            const A = x - wall.x1;
            const B = y - wall.y1;
            const C = wall.x2 - wall.x1;
            const D = wall.y2 - wall.y1;
            const dot = A * C + B * D;
            const len_sq = C * C + D * D;
            let param = -1;
            if (len_sq != 0) param = dot / len_sq;

            let xx, yy;
            if (param < 0) {
                xx = wall.x1;
                yy = wall.y1;
            } else if (param > 1) {
                xx = wall.x2;
                yy = wall.y2;
            } else {
                xx = wall.x1 + param * C;
                yy = wall.y1 + param * D;
            }

            const dist = Math.hypot(x - xx, y - yy);
            return dist > 15; // Apaga se estiver a menos de 15px da linha
        });

        // Remove também se clicou em um equipamento no modo borracha
        equipments = equipments.filter(eq => {
            const dist = Math.hypot(eq.x - x, eq.y - y);
            return dist > 20;
        });

        updateSummary();
        drawAll();
    }

    function drawAll() {
        // Limpar tela
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Desenhar Grid de apoio
        ctx.beginPath();
        ctx.strokeStyle = '#f1f1f1';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 20) {
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
        }
        for (let y = 0; y < canvas.height; y += 20) {
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
        }
        ctx.stroke();

        // Desenhar Paredes
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
        walls.forEach(wall => {
            ctx.beginPath();
            ctx.moveTo(wall.x1, wall.y1);
            ctx.lineTo(wall.x2, wall.y2);
            ctx.stroke();
        });

        // Desenhar Equipamentos colocados
        equipments.forEach(eq => {
            const config = eqConfig[eq.type];
            
            // Desenhar círculo de fundo
            ctx.beginPath();
            ctx.arc(eq.x, eq.y, 16, 0, 2 * Math.PI);
            ctx.fillStyle = config.color;
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#ffffff';
            ctx.stroke();

            // Desenhar sombra
            ctx.beginPath();
            ctx.arc(eq.x, eq.y, 18, 0, 2 * Math.PI);
            ctx.strokeStyle = 'rgba(0,0,0,0.1)';
            ctx.lineWidth = 1;
            ctx.stroke();

            // Desenhar Ícone/Texto interno
            ctx.font = 'bold 12px sans-serif';
            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(config.text, eq.x, eq.y);
        });
    }

    function updateSummary() {
        const counts = {};
        equipments.forEach(eq => {
            counts[eq.type] = (counts[eq.type] || 0) + 1;
        });

        const container = document.getElementById('equipment-count');
        if (equipments.length === 0) {
            container.innerHTML = "Nenhum equipamento inserido ainda.";
            return;
        }

        let html = '<ul style="margin: 0; padding-left: 15px; font-size:12px;">';
        for (const [type, count] of Object.entries(counts)) {
            html += `<li><strong>${count}x</strong> ${eqConfig[type].label}</li>`;
        }
        html += '</ul>';
        container.innerHTML = html;
    }

    function clearCanvas() {
        if(confirm("Deseja realmente limpar todo o desenho e recomeçar?")) {
            walls = [];
            equipments = [];
            updateSummary();
            drawAll();
        }
    }
</script>

</body>
</html>
"""

# Renderizar o Canvas HTML interativo na tela
st.markdown("### 🗺️ Desenhe e Planeje a Segurança do Imóvel")
components.html(canvas_html, height=650, scrolling=True)

# Área de fechamento e detalhamento de valores
st.markdown("---")
st.markdown("### 💰 Proposta Comercial Estimada")

col1, col2, col3 = st.columns(3)

with col1:
    valor_mensal = st.slider("Valor do Monitoramento Mensal (R$)", min_value=99, max_value=350, value=149, step=10)
    st.markdown(f"**Valor de Manutenção e Monitoramento da Central Orsegups 24h:** R$ {valor_mensal}/mês")

with col2:
    custo_instalacao = st.selectbox("Custo de Ativação / Instalação", ["Grátis (Ação Promocional na Rua)", "R$ 99,00", "R$ 199,00"])
    st.markdown(f"**Ativação de Equipamento com Garantia Vitalícia:** {custo_instalacao}")

with col3:
    prazo = st.selectbox("Tempo de Contrato", ["Sem Fidelidade", "12 Meses", "24 Meses"])
    st.markdown(f"**Fidelidade do Plano:** {prazo}")

st.markdown("---")

# Seção de exportação/fechamento rápido
st.subheader("✍️ Conclusão da Proposta")
if nome_cliente:
    st.success(f"**Proposta personalizada gerada com sucesso para: {nome_cliente}!**")
    st.markdown(f"""
    **Resumo Técnico da Proposta Comercial - Orsegups Alarme 365**
    
    *   **Cliente:** {nome_cliente}
    *   **Tipo do Imóvel:** {tipo_imovel}
    *   **Tecnologia Proposta:** Sistema Alarme 365 sem fio com sensores de verificação de imagem, SOS integrado, áudio interativo e garantia vitalícia.
    *   **Mensalidade de Monitoramento 24h:** R$ {valor_mensal},00
    *   **Taxa de Ativação:** {custo_instalacao}
    *   **Prazo contratual:** {prazo}
    
    *Próximo passo: Agendar o horário do vistoriador técnico credenciado da Orsegups para realizar a homologação e instalação definitiva.*
    """)
    if st.button("Copiar Proposta Comercial para Área de Transferência"):
        st.toast("Proposta copiada! Pronto para enviar no WhatsApp ou colar em seu CRM.", icon="✅")
else:
    st.warning("Preencha o Nome do Cliente na barra lateral esquerda para ativar o gerador de propostas!")
