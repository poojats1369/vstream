def genre_code_generate(genre_name):
    split_string = genre_name.split() 
    genre_code = "-".join(split_string) 
    return genre_code