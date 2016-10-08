from conversion_manager import ConversionManager

cm = ConversionManager()
cm.load_plugins('plugins')

# delim_reader_lines -> validate_process
pi = cm.getClassByName("delim_reader_lines")()
po = cm.getClassByName("validate_process")()
pi.set_config({"file_path":"tests/delimitado1.txt.orig", "delimiter":"|","quotechar":'"',"encoding":""})
po.set_config({"allow_nulls":[True, True, True, False],"formats":["NA","DDMMYYYY","#","#.#"],"skip":1})
print(cm.line_count(pi))
print(cm.transform(pi,po))


# delim_reader_lines -> delim_writter_lines
pi = cm.getClassByName("delim_reader_lines")()
po = cm.getClassByName("delim_writer_lines")()
pi.set_config({'file_path':'tests/delimitado1.txt.orig', 'delimiter':'|','quotechar':'"','encoding':''})
po.set_config({'file_path':'tests/delimitado2.txt', 'delimiter':',','quotechar':'"','encoding':''})
print(cm.transform(pi,po))

# delim_reader_lines -> json_writer_lines
pi = cm.getClassByName("delim_reader_lines")()
po = cm.getClassByName("json_writer_lines")()
pi.set_config({'file_path':'tests/delimitado2.txt', 'delimiter':',','quotechar':'"','encoding':''})
po.set_config({'file_path':'tests/json1.txt', 'encoding':''})
print(cm.transform(pi,po))

# json_reader_lines -> fixed_writer_lines
pi = cm.getClassByName("json_reader_lines")()
po = cm.getClassByName("fixed_writer_lines")()
pi.set_config({'file_path':'tests/json1.txt', 'encoding':''})
po.set_config({'file_path':'tests/fixed_lines1.txt', 'tamanios':[40,20,10,10],'orientations':['l','r','r','r'],'encoding':''})
print(cm.transform(pi,po))

# fixed_reader_lines -> fixed_writer_chunks
pi = cm.getClassByName("fixed_reader_lines")()
po = cm.getClassByName("fixed_writer_chunks")()
pi.set_config({'file_path':'tests/fixed_lines1.txt', 'tamanios':[40,20,10,10],'encoding':''})
po.set_config({'file_path':'tests/fixed_chunks1.txt', 'tamanios':[40,20,10,10],'orientations':['l','r','r','r'],'encoding':''})
print(cm.transform(pi,po))

# fixed_reader_chunks -> delim_writer
pi = cm.getClassByName("fixed_reader_chunks")()
po = cm.getClassByName("delim_writer_lines")()
pi.set_config({'file_path':'tests/fixed_chunks1.txt', 'tamanios':[40,20,10,10],'encoding':''})
po.set_config({'file_path':'tests/delimitado3.txt', 'delimiter':'|','quotechar':'"','encoding':''})
print(cm.transform(pi,po))
