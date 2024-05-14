from models import Author, Quote
import connect, json
author_file='authors.json'
quote_file = 'quotes.json'
  
def add_author(el):
    print(el['fullname'])
    author= Author(fullname = el['fullname'],
    born_date=el['born_date'],
    born_location=el['born_location'],
    description=el['description'])
    return author

def add_quote(item, author_object ):
    tags = [tag for tag in item['tags']]
    quote_ob = Quote(tags=tags,
        author= author_object,
        quote=item['quote'])
    return quote_ob


if __name__=="__main__":
    # with open(author_file, 'r') as f:
    #     json_author = json.load(f)
    # for el in json_author:
    #     author = add_author(el)
    #     author.save()
    # find_autor:dict = Author.objects(fullname='Albert Einstein')

    with open(quote_file, 'r') as f:
        json_quote = json.load(f)
    for item in json_quote:
        aut_name = item['author']
        find_autor:dict = Author.objects(fullname=aut_name)
        if find_autor:
            for i  in find_autor:
                new_tag = add_quote(item, i)
                new_tag.save()
        else:
            print('ERROR: Can\'t find this author\'s name')


    notes = Author.objects()
    print("-------------------")
    for note in notes:
        print(note.to_mongo().to_dict())

    otes = Quote.objects()
    print("-------------------")
    for note in otes:
        print(note.to_mongo().to_dict())


    # ''''''
    # quot = Quote.objects()
    # for q in quot:
    #     q.delete()

