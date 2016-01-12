#!/usr/bin/env python
import yaml
import pystache
import json
import pprint

def truncword(content, length, suffix):
    return content if len(content) <= length else content[:length-len(suffix)].rsplit(' ', 1)[0] + suffix

with open("CitySDK-palaute.yaml") as stream:
    apidoc = yaml.safe_load(stream)

with open("palaute-graph.gvt") as stream:
    template = stream.read()

defs = apidoc['definitions']

context = []

for definition in defs:
    formatted = {}
    # Need to replace pystache with something more capable, but too tired
    formatted['name'] = definition
    keys = ['title', 'description']
    for k in keys:
        if k in defs[definition]:
            formatted[k] = defs[definition][k]
    
    formatted['properties'] = []
    
    for prop in defs[definition]['properties']:
        property = defs[definition]['properties'][prop]
        if 'title' in property:
            desc = property['title']
        elif 'description' in property:
            desc = property['description']
        else:
            desc = prop
        
        formatted['properties'].append({'name': prop, 'description': truncword(desc, 60, "...")})
        
    context.append(formatted)

rendis = pystache.Renderer(string_encoding='utf-8', missing_tags="strict")

print rendis.render(template, {'c': context}).encode('utf-8')
