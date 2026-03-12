import argparse
import os
import logging

from dotenv import load_dotenv

from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers

_logger = logging.getLogger(__name__)


class DocumentSigner:

    def __init__(self, pdf_path, cert_pfx_path):
        load_dotenv()

        cert_pass = os.getenv("CERT_PASS", "")
        # Validate certificate environment variables
        if not cert_pfx_path:
            raise RuntimeError("Environment variable CERT_PFX is not set")
        if os.path.isfile(cert_pfx_path) is False:
            raise RuntimeError(f"Certificate file not found at path: {cert_pfx_path}")
        if not cert_pass:
            raise RuntimeError("Environment variable CERT_PASS is not set")
        self.pdf_path = pdf_path

        self.signer = signers.SimpleSigner.load_pkcs12(
            pfx_file=cert_pfx_path,
            passphrase=cert_pass.encode()
        )
        _logger.info(f"Loaded signer from PKCS#12 file: {cert_pfx_path}")
                    
    def sign_document(self, output_path):
        with open(self.pdf_path, "rb") as doc:
            w = IncrementalPdfFileWriter(doc)
            
            metadata = signers.PdfSignatureMetadata(field_name='Signature1')

            signed_data = signers.sign_pdf(
                w,
                metadata,
                signer=self.signer,
            )

            with open(output_path, 'wb') as output_doc:
                output_doc.write(signed_data.read())
            
        _logger.info("PDF assinado com sucesso!")
            
        
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    _logger.info("Iniciando o processo de assinatura de documento PDF")
    load_dotenv()

    parser = argparse.ArgumentParser(description="Assinar um documento PDF")
    parser.add_argument(
        "-p",
        "--pdf_path",
        required=True,
        help="Caminho para o documento PDF a ser assinado"
    )
    # Make output_path an optional positional argument
    parser.add_argument(
        "-o",
        "--output_path",
        help="Caminho para salvar o documento PDF assinado"
    )
    parser.add_argument(
        "-c",
        "--cert_pfx_path",
        help="Caminho para o arquivo PKCS#12 (.pfx) contendo o certificado e a chave privada"
    )
    args = parser.parse_args()
    
    pdf_path = args.pdf_path
    cert_pfx_path = args.cert_pfx_path or os.getenv("CERT_PFX", "")
    # If output_path not provided, append _signed before extension
    output_path = args.output_path or os.path.splitext(pdf_path)[0] + "_signed.pdf"

    signer = DocumentSigner(pdf_path, cert_pfx_path)
    signer.sign_document(output_path)