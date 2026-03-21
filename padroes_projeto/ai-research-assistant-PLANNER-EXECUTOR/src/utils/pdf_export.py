# src/utils/pdf_export.py
import os
import re
from datetime import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    """Classe personalizada para adicionar cabeçalho e rodapé automáticos no PDF."""
    def header(self):
        # Configura a fonte (Helvetica, Negrito, tamanho 14)
        self.set_font("helvetica", "B", 14)
        # Título centralizado
        self.cell(0, 10, "Relatório de Pesquisa Autônoma (IA)", align="C")
        # Quebra de linha
        self.ln(15)

    def footer(self):
        # Posiciona a 1.5 cm do final da página
        self.set_y(-15)
        # Fonte menor e em itálico para o rodapé
        self.set_font("helvetica", "I", 8)
        # Número da página
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

def save_report_to_pdf(topic: str, content: str) -> str:
    """
    Recebe o tema e o conteúdo do relatório, gera um PDF e salva na pasta 'relatorios'.
    Retorna o caminho do arquivo gerado.
    """
    # 1. Garante que a pasta 'relatorios' existe na raiz do projeto
    output_dir = "relatorios"
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. Formata a data e limpa o tema para usar como nome de arquivo
    date_str = datetime.now().strftime("%d-%m")
    
    # Remove caracteres especiais do tema que poderiam quebrar o nome do arquivo no Windows/Linux
    safe_topic = re.sub(r'[^a-zA-Z0-9 \-_]', '', topic).strip()
    
    # Monta o nome final do arquivo
    filename = f"Relatório - {safe_topic} - {date_str}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # 3. Cria e configura o PDF
    pdf = PDFReport()
    pdf.add_page()
    
    # Usamos uma fonte padrão que suporta bem caracteres latinos
    pdf.set_font("helvetica", size=11)
    
    # 4. Escreve o conteúdo. 
    # multi_cell lida automaticamente com quebras de linha de textos grandes.
    # OBS: Como o LLM gera Markdown, asteriscos de negrito (**) vão aparecer no texto.
    pdf.multi_cell(0, 7, text=content)
    
    # 5. Salva o arquivo fisicamente
    pdf.output(filepath)
    
    return filepath