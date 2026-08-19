from typing import Optional, Dict, Any
import re
from datetime import datetime

class OCRService:
    """
    Serviço OCR para extração de dados de faturas de energia
    """

    @staticmethod
    def extrair_dados_fatura(texto_ocr: str) -> Dict[str, Any]:
        """
        Extrai dados de uma fatura de energia a partir do texto OCR
        """
        dados = {}

        # Padrões de extração (exemplo - ajuste conforme necessidade)
        padroes = {
            "numero_fatura": r"FATURA\s*N[º°]\s*(\d+)",
            "codigo_barras": r"(\d{44})",
            "mes_referencia": r"REFERENTE\s*A\s*(\d{2}/\d{4})",
            "data_vencimento": r"VENCIMENTO\s*(\d{2}/\d{2}/\d{4})",
            "consumo_kwh": r"CONSUMO\s*(\d+[,.]?\d*)\s*KWH",
            "valor_total": r"TOTAL\s*A\s*PAGAR.*?R\$\s*([0-9,.]+)",
            "valor_tusd": r"TUSD.*?R\$\s*([0-9,.]+)",
            "valor_te": r"TE.*?R\$\s*([0-9,.]+)",
            "valor_bandeira": r"BANDEIRA.*?R\$\s*([0-9,.]+)",
            "valor_iluminacao_publica": r"ILUMINAÇÃO.*?R\$\s*([0-9,.]+)",
        }

        for campo, padrao in padroes.items():
            match = re.search(padrao, texto_ocr, re.IGNORECASE)
            if match:
                valor = match.group(1)
                if campo in ["mes_referencia", "data_vencimento"]:
                    try:
                        dados[campo] = datetime.strptime(valor, "%m/%Y").date() if campo == "mes_referencia" else datetime.strptime(valor, "%d/%m/%Y").date()
                    except:
                        pass
                elif campo in ["consumo_kwh", "valor_total", "valor_tusd", "valor_te", "valor_bandeira", "valor_iluminacao_publica"]:
                    try:
                        dados[campo] = float(valor.replace(".", "").replace(",", "."))
                    except:
                        pass
                else:
                    dados[campo] = valor

        return dados

    @staticmethod
    def processar_fatura(texto_ocr: str) -> Optional[Dict[str, Any]]:
        """
        Processa a fatura e retorna dados estruturados
        """
        try:
            dados = OCRService.extrair_dados_fatura(texto_ocr)

            if not dados.get("valor_total") or not dados.get("consumo_kwh"):
                return None

            return dados
        except Exception as e:
            print(f"Erro ao processar fatura: {e}")
            return None

# Mantendo compatibilidade com importações antigas
ExtratorFaturaEnergia = OCRService