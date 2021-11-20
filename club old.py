def parsing_from_page_club(url):
    count_clubs = 0

    req = requests.get(list_url[i], headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    clubs = soup.find(class_='items').find_all(class_='hauptlink no-border-links show-for-small show-for-pad')

    for j in clubs:

        print(j.text)

        if id != None and id not in store['clubs_link'].keys():
            count_clubs += 1
            store['clubs_link'][id] = {'url': getFullURL(j.get('href')), 'name': j.text}


    print(f"Собрано {count_clubs} клубов")
    time.sleep(randrange(1,3))