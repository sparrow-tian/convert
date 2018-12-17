#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import logging, os, argparse, textwrap
import time
import chardet
import re
 
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
 
 
class Convert2Utf8:
    def __init__(self, args):
        self.args = args
 
 
 
    def convert_file(self, filename):
        with open(filename, 'rb') as f: # read under the binary mode
            bytedata = f.read()
 
        if len(bytedata) == 0:
            log.info("Skipped empty file %s", filename)
            return
 
        chr_res = chardet.detect(bytedata)
        if chr_res['encoding'] == None or chr_res['confidence'] < 0.9:
            log.warning("Ignoring %s, since its encoding is unable to detect.", filename)
            return
 
        src_enc = chr_res['encoding'].lower()
        log.debug("Scanned %s, whose encoding is %s ", filename, src_enc)
        if src_enc.startswith('utf'):
            log.info("Skipped %s, whose encoding is %s", filename, src_enc)
            return
 
 
        # Since chardet only recognized all GB-based target_encoding as 'gb2312', the decoding will fail when the text file
        # contains certain special charaters. To make it more special-character-tolerant, we should
        # upgrade the target_encoding to 'gb18030', which is a character set larger than gb2312.
        if src_enc.lower() == 'gb2312':
            src_enc = 'gb18030'
 
        try:
            strdata = bytedata.decode(src_enc)
        except UnicodeDecodeError as e:
            log.error("Unicode error for file %s", filename)
            print(e)
            return
 
 
        tgt_enc = self.args.target_encoding
        log.debug("Writing the file: %s in %s", filename, tgt_enc)
        with open(filename, 'wb') as f: # write under the binary mode
            f.write(strdata.encode(tgt_enc))
        log.info("Converted the file: %s from %s to %s", filename, src_enc, tgt_enc)
 


 
    def run(self):
        xml = self.args.xml
        if not os.path.exists(xml):
            log.error("The file specified %s is neither a directory nor a regular file", xml)
            return
 
        log.info("Start working now!")
 
        if os.path.isdir(xml):
            log.info("The xml is: %s. ", xml)
            log.info("Not support directory yet!")
        else:
            log.info("Only a single file will be processed: %s", xml)
            self.convert_file(xml)
 
        log.info("Finished all.")
 
 
 
def cli():
    parser = argparse.ArgumentParser()
 
    parser.add_argument(
        'xml',
        metavar = "filename",
        help    = textwrap.dedent('''\
            the path pointing to the file or directory(not support yet).
            If it's a directory, files contained in it with specified extensions will be converted to UTF-8.
            Otherwise, if it's a file, only that file will be converted to UTF-8.''')
        )
 
 
 
    args = parser.parse_args()
 
 
    args.target_encoding = 'utf-8'
 
    cvt2utf8 = Convert2Utf8(args)
    cvt2utf8.run()
 
if __name__ == '__main__':
    cli()

