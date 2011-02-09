def save_claims(claims):
    file_content = ''
    for build, person in claims.iteritems():
        file_content += build + "::::" + person + "\n"
    f = open("peopleworkingonbuilds.txt", "w")
    f.write(file_content)
    f.close()

def get_claims_as_hash():
    claims = {}
    f = open("peopleworkingonbuilds.txt", 'r')
    lines = f.readlines()
    if len(lines) == 0:
        return {}
    for line in lines:
        try:
            build, person = line.split("::::")
            claims[build.strip()] = person.strip()
        except:
            #not a valid line apparently
            pass
    return claims
