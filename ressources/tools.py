#!/usr/bin/python3

def saves_pictures(UPLOAD_FOLDER,image,app,users = False): 
        import os
        from datetime import datetime
        current_time = datetime.now().strftime("%y-%m-%d_%H-%M-%S")
        #stockage - imgage
        
        if users is not False :
            save_path = UPLOAD_FOLDER+ "/" + users
            
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            stockage = save_path +"/" +str(current_time)
        else :
            save_path = UPLOAD_FOLDER+ "/"
            stockage = save_path +"/" +str(current_time)

        # save local
        filename = stockage + ".jpg"
        image.save(os.path.join(app.root_path, filename))
        return filename
        
def translate_encode(txt):
    import re
    txt = re.sub("\d"," ",txt)

    return txt


def translate(texte,dest = 'fr', short = False) :
    """
    texte = Your text to translate
    dest = to language defaut french
    """        

    from google_trans_new import google_translator  
    
    translator = google_translator()

    if short is True :
        translate_text = translator.translate(translate_encode(texte), lang_src='en', lang_tgt=dest)
    else :
        translate_text = translator.translate(texte, lang_src='en', lang_tgt=dest)

    return translate_text


def request_food_local(recherche = False, flask = False, type_pred = "fruits"):
    """
    recherche : False for all df : True for Only name, str for specifique research
    """
    from pandas import read_excel
    df = read_excel("ressources/data/Table Ciqual 2020_FR_2020 07 07.xls", header =  0)

    df = df[df['alim_ssgrp_nom_fr']== type_pred]



    cols_id = ["alim_grp_code","alim_ssgrp_code","alim_ssssgrp_code"]
    to_drop = cols_id
    clean_df = df.drop(columns = to_drop)

    if recherche is False :
        return df
    elif recherche is True : 
        return df['alim_nom_fr']
    else :
        if flask is True :
            #Result = clean_df[clean_df['alim_nom_fr'].str.contains(recherche)].transpose()
            Result = clean_df[clean_df['alim_nom_fr'].str.contains("Pomme")].transpose() #### FOR TEST
            columns = Result.columns.values


            row = [Result.to_html(classes='data')] 
            return columns,row
        else : 
            return ""
