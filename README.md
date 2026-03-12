# Document Signer - Exemplo com pyHanko 0.34.1

Este repositório contém um exemplo simples (`teste.py`) que assina um PDF usando a biblioteca pyHanko v0.34.1 e um certificado A1 em PKCS#12 (.p12/.pfx).

Conteúdo relevante
- `teste.py` - script de exemplo para assinar um PDF.
- `requirements.txt` - dependências sugeridas (pyHanko==0.34.1).

Pré-requisitos
- Python 3.8+
- Um certificado A1 exportado como PKCS#12 (.p12 ou .pfx) com a senha correspondente.

Instalação (recomendado em ambiente virtual)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Uso básico

- Com argumentos explícitos (arquivo PDF, certificado e senha):

```bash
python3 teste.py -p ./documento.pdf -c /caminho/para/cert.p12 -w minha_senha -o ./documento_assinado.pdf
```

- Usando variáveis de ambiente (ou um `.env` com `CERT_PFX` e `CERT_PASS`):

```bash
export CERT_PFX=/caminho/para/cert.p12
export CERT_PASS=minha_senha
python3 teste.py -p ./documento.pdf
# cria ./documento_signed.pdf por padrão
```

Explicação rápida do `teste.py`
- Valida a existência do PDF de entrada e do arquivo PKCS#12.
- Lê a senha do `--cert-pass` ou da variável de ambiente `CERT_PASS`.
- Utiliza `PKCS12Signer.from_p12_file` para carregar o certificado e a chave.
- Cria um `PdfSigner` e assina o documento gerando um novo arquivo.

Nota sobre IDEs e "Unresolved import"
- Se a sua IDE mostrar um aviso tipo "Unresolved import: PKCS12Signer", isso normalmente significa que a biblioteca não está instalada no mesmo ambiente que a IDE usa para análise estática. Instale as dependências no ambiente usado pela IDE ou ignore o aviso se o script executar corretamente no terminal após instalar as dependências.

Erros e mensagens úteis
- "Input PDF not found" — verifique o caminho do PDF de entrada.
- "PKCS#12 file not found" — verifique o caminho do certificado.
- "senha do PKCS#12" — informe a senha via `--cert-pass` ou `CERT_PASS`.

Próximos passos possíveis (posso ajudar a implementar)
- Adicionar aparência visual da assinatura (posição/retângulo e imagem).
- Incluir timestamp via TSA.
- Validar cadeia de certificação (OCSP/CRL) após a assinatura.

Se quiser que eu implemente alguma das opções acima, diga qual preferiria primeiro.