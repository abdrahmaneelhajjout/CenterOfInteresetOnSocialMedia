
def start(url):
    import config
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    import time
    import importlib
    import os
    from IPython import get_ipython
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
    # In[8]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 8")
    importlib.reload(config)
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        f"{config.webDriverPath}", options=options)

    driver.get("https://www.facebook.com")

    email = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    email.clear()
    password.clear()
    email.send_keys(f"{config.username}")
    password.send_keys(f"{config.password}")
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()

    # In[27]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 27")
    time.sleep(2)
    photos_Url = []  # pour contenir la list des albums
    images = []  # pour contenir la liste des liens des images dans tous les album
    all_images = []
    dir(config)
    driver.get(f"{url}/photos")
    time.sleep(1)

    photos_Url = driver.find_elements_by_tag_name('a')
    # list(set(obj)) pour supprimer les élements redondantes d'une liste obj
    photos_Url = list(set([i.get_attribute('href') for i in photos_Url if i.get_attribute(
        'href') is not None and i.get_attribute('href').startswith(f"{url}/photo")]))

    # recuperer la liste qui contient juste les lien des albums contenant les images
    for photoPage in photos_Url:
        driver.get(photoPage)
        albums = [i.get_attribute('href') for i in driver.find_elements_by_tag_name('a') if i.get_attribute(
            'href') is not None and i.get_attribute('href').startswith("https://www.facebook.com/media/set/?set")]
        if len(albums) > 0:
            # supprimer l'elemnt qui contient les albums puis les remplacer avec les lien des albums.
            photos_Url.remove(photoPage)
            photos_Url.extend(albums)

    # In[29]:---------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 29")
    images = []
    for album in photos_Url:
        driver.get(album)  # naviguer vers le lien
        time.sleep(1)  # attente un peu
        imgs = driver.find_elements_by_tag_name("a")
        if imgs is not None:
            for img in imgs:
                if img.get_attribute('href') is not None and img.get_attribute('href').startswith("https://www.facebook.com/photo"):
                    images.append(img.get_attribute('href'))

    all_images.extend(list(set(images)))

    # In[40]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 40")
    all_images = list(set(all_images))
    img_url = []

    for img in all_images:
        driver.get(img)
        image = driver.find_elements_by_tag_name("img")
        if len(image) > 0:
            img_url.append(image[0].get_attribute('src'))

    img_url = list(set(img_url))

    # In[57]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 57")

    import os
    import shutil

    path = os.getcwd()
    path = os.path.join(path, "Facebook_Images")
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)

    # In[58]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 58")
    import wget

    # download images
    counter = 0
    try:
        for image in img_url:
            save_as = os.path.join(path, str(counter) + '.jpg')
            wget.download(image, save_as)
            counter += 1
    except Exception as e:
        print(str(e))

    # In[84]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    print("in 84")

    # The glob module finds all the pathnames matching a specified pattern according to the rules used by OS
    import glob

    f = open("train.txt", "w")
    for file in glob.glob("Facebook_Images\\*.jpg"):
        f.write(file)
        f.write("\n")
    f.close()

    # In[85]:--------------------------------------------------------------------------------------------------------------------------------------------------------------
    # recuperer une instance d'un terminal interactive
    shell = TerminalInteractiveShell.instance()
    # lancer la commande dans le terminal qu'on a créer
    get_ipython().system('F:\\darknet\\darknet-master\\build\\darknet\\x64\\darknet.exe detector test coco.data yolov4.cfg yolov4.weights -dont_show -ext_output < train.txt > result.txt')

    # regular expression module
    import re

    var1 = list()
    var2 = list()
    numobj = list()
    numobj0 = list()

    # extracting data, get classnames that are present in our file
    file = open("result.txt", "rt")
    for line in file:
        i = re.findall(r'^[a-z]*:', line)
        var1.append(i)
    file.close()

    # remove the empty blanks
    for x in var1:
        if x != []:

            var2.append(x)

    # remove the duplicated item
    objdetec = []
    for item in var2:
        if item not in objdetec:
            objdetec.append(item)

    # count every object
    for el in objdetec:
        cout = 0
        for el1 in var2:
            if el1 == el:
                cout += 1
        numobj0.append(cout)
    print('before returning')
    driver.quit()
    return zip(numobj0, objdetec)

# ---------------------- zip() method test----------------------
#languages = ['Java', 'Python', 'JavaScript']
#versions = [14, 3, 6]

#result = zip(languages, versions)
# print(list(result))
# Output: [('Java', 14), ('Python', 3), ('JavaScript', 6)]
