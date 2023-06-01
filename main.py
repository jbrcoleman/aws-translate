"""
Command line tool that utilizes aws translate
to translate a file.
"""

import click
import boto3
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)

PROFILE = "test-go"
session = boto3.Session(
    region_name="us-east-1",
    profile_name=PROFILE,
)
translate_client = session.client("translate")


@click.command()
@click.option(
     "--source_language_code", default="en", help="Language of source file."
)
@click.option(
    "--target_language_code", help="Language source file will be translated to."
)
@click.option("--source_file", help="Path of source file that will be translated.")
def translate(source_language_code, target_language_code, source_file):
    """
    This function translates the source file to from the
    source language to the target language.
    """
    data = open_file(source_file)
    log.info("File %s opened", source_file)
    try:
        result = translate_client.translate_document(
            Document={"Content": data, "ContentType": "text/html"},
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )
    except Exception as e:
        log.error(e)
        raise
    translated_file = write_document(source_file, result)
    log.info("Translated document: %s", translated_file)


def open_file(source_file):
    """
    This function opens the source file.
    """
    localFile = source_file
    file = open(localFile, "rb")
    data = file.read()
    file.close()
    return data


def write_document(source_file, translate_result):
    """
    This function pulls the translated result from
    aws response.
    """
    if "TranslatedDocument" in translate_result:
        file_name = source_file.split("/")[-1]
        tmp_file = f"translated.{file_name}"
        with open(tmp_file, "w", encoding="utf-8") as f:
            f.write(str(translate_result["TranslatedDocument"]["Content"]))
        return tmp_file
    log.error("No Translated Document found in response")

if __name__ == '__main__':
    translate()