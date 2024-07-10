

def main():
    domains = {}
    with open('blocked_domains.txt') as f:
        for domain in f.readlines():
            domain = domain.strip()
            if domain not in domains:
                domains[domain] = 1
            else: domains[domain] += 1
    sortedDomains = sorted(domains.items(), key= lambda x: -x[1])
    print('\nThe most common 10 domains are:')
    for i in range(5):
        print(sortedDomains[i][0] + ' cu frecventa: ' + str(sortedDomains[i][1]))
    googleDomains = [(d, f) for d, f in sortedDomains if 'google' in d]
    nrGoogle = sum([x for _, x in googleDomains])
    facebookDomains = [(d, f) for d, f in sortedDomains if 'facebook' in d]
    nrFacebook = sum([x for _, x in facebookDomains])
    nrDomains = sum([x for _, x in sortedDomains])
    print("\nNumarul total de domenii: " + str(nrDomains))
    print("\nNumarul domenii Google: " + str(nrGoogle) + ', ' +str(int(nrGoogle / nrDomains * 10000)/100)+f'% din numarul de domenii' )
    print("\nNumarul domenii Facebook: " + str(nrFacebook) + ', ' +str(int(nrFacebook / nrDomains * 10000)/100)+f'% din numarul de domenii' )


main()        
