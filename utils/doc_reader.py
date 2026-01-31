from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os
import shutil

class DocLoader:
    def extract_resume_text(self, resume_file_path: str) -> str:
        loader = PyPDFLoader(resume_file_path)
        pages = loader.load()
        return " ".join([page.page_content for page in pages])

    def extract_jd_text(self, jd_file_path: str) -> str:
        loader = TextLoader(jd_file_path)
        pages = loader.load()
        return " ".join([page.page_content for page in pages])
