import re
import connect
from models import Author, Quote
from mongoengine.errors import DoesNotExist

def parser(pars):
    pattern = r":"
    if re.search(pattern, pars):
        command, args = re.split(pattern, pars)
        return command.strip().lower(), args.strip()
    else:
        return pars.strip().lower(), None
    

def arg_parser(args):
    if args ==1:
        return args.strip().lower()
    else:
        patt = r','
        args = re.split(patt, args, maxsplit=3)
        return args


def search_quotes_by_author(author_name):
    try:
        author_obj = Author.objects(fullname__icontains=author_name)
        for item in author_obj:
            quotes = Quote.objects(author=item.id)
        return quotes
    except DoesNotExist:
        return []
    

def search_quotes_by_tag(tag_names):
    try:
        if ',' in tag_names:
            n = tag_names.split(',')
            quotes = Quote.objects(tags__in=n)
            if quotes: 
                return quotes
            else:
                print('cannot found this tag')
                return None
        else:
            quotes = Quote.objects(tags__icontains=tag_names)
            if quotes: 
                return quotes
            else:
                print('cannot found this tag')
                return None
            
    except DoesNotExist:
        print('ERROR: does not exist')
        return []



def main():
    print('WELCOME to QuoteSearch.\nlet\'s start\ni have a help-list for beginners')
    try:
        print('please, give me some points to start\nformat: \'tag:life\'')
        while True:
            pars = input('enter: ')
            command, args = parser(pars)
            if command =='exit':
                break
            elif command=='tag':
                info = search_quotes_by_tag(args)
                for i in info:
                    print('-------')
                    print(i.quote)
                    print('-------')
            elif command=='tags':
                info =  search_quotes_by_tag(args)   
                for i in info:
                    print('-------')
                    print(i.quote)
                    print('-------')
            elif command=='name':
                info = search_quotes_by_author(args)
                for i in info:
                    print('-------')
                    print(i.quote)
                    print('-------')
            else:
                print('maybe i have not this command. try again')
    except Exception as e:
        print(f'it seems to be something wrong: {e}')

if __name__=='__main__':
    main()