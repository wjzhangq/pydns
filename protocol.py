# -*- coding:utf-8 -*-
import struct
from cStringIO import StringIO

class Header(object):
    
    def __init__(self, id, flags, questions, answer_rrs, authority_rrs, additional_rrs):
        self.id = id
        self.flags = flags
        self.questions = questions
        self.answer_rrs = answer_rrs
        self.authority_rrs = authority_rrs
        self.additional_rrs = additional_rrs
        
    @classmethod
    def parse(cls, data):
        id, flags, questions, answer_rrs, authority_rrs, additional_rrs = struct.unpack('!6H', data.read(12))
        return Header(id, flags, questions, answer_rrs, authority_rrs, additional_rrs)
         
    def serialize(self, data):
        data.write(struct.pack('!6H', self.id, self.flags, self.questions, self.answer_rrs, self.authority_rrs, self.additional_rrs))
        
    def __str__(self):
        return '{id: %s, flags: %s, questions: %s, answer_rrs: %s, authority_rrs: %s, additional_rrs: %s}' % (
            self.id, self.flags, self.questions, self.answer_rrs, self.authority_rrs, self.additional_rrs)

class Query(object):
    
    TYPE_A = 1
    TYPE_AAAA = 28
    CLASS_IN = 1
    
    def __init__(self, name, type, clazz):
        self.name = name
        self.type = type
        self.clazz = clazz
        
    @classmethod
    def parse(cls, data):
        domain = cls._parse_domain_name(data)
        type, clazz = struct.unpack('!2H', data.read(4))
        return Query(domain, type, clazz)
    
    def serialize(self, data):
        self._serialize_domain_name(data)
        data.write(struct.pack('!2H', self.type, self.clazz))
        
    @staticmethod
    def _parse_domain_name(data):
        list = []
        while True:
            tmp = data.read(1)
            len = ord(tmp)
            if len == 0:
                break
            list.append(data.read(len))
        return '.'.join(list)

    def _serialize_domain_name(self, data):
        list = self.name.split('.')
        for i in list:
            data.write(struct.pack('!B%ss' % (len(i)), len(i), i))
        data.write(struct.pack('!B', 0))

    def __str__(self):
        return '{name: %s, type: %s, class: %s}' % (
            self.name, self.type, self.clazz) 

class Answer(Query):
    
    def __init__(self, name, type, clazz, ttl, data):
        Query.__init__(self, name, type, clazz)
        self.ttl = ttl
        self.data = data
        
    def serialize(self, data):
        data.write(struct.pack('!2B', 0xc0, 0x0c))
        data.write(struct.pack('!2HI', self.type, self.clazz, self.ttl))
        #only support A
        if self.type == Answer.TYPE_A:
            addr = self.data.split('.')
            data.write(struct.pack('!H', len(addr)))
            for i in addr:
                data.write(struct.pack('!B', int(i)))

    def __str__(self):
        return '{name: %s, type: %s, class: %s, ttl: %s, data_length: %s, data: %s}' % (
            self.name, self.type, self.clazz, self.ttl, self.data_length, self.data) 

class DnsRequest(object):
    
    def __init__(self, header, queries=[]):
        self.header = header
        self.queries = queries

    @classmethod
    def parse(cls, data):
        header = Header.parse(data)
        queries = []
        for _ in range(header.questions):
            queries.append(Query.parse(data))
        return DnsRequest(header, queries)
    
    def serialize(self):
        data = StringIO()
        self.header.serialize(data)
        for i in range(len(self.queries)):
            self.queries[i].serialize(data)
        data.seek(0)
        return data.read()

    def __str__(self):
        return '{header: %s, queries: %s}' % (
            self.header, str(self.queries))
        
class DnsResponse(object):
    
    def __init__(self, header, queries=[], answers=[]):
        self.header = header
        self.queries = queries
        self.answers = answers

    def serialize(self):
        data = StringIO()
        self.header.serialize(data)
        for q in self.queries:
            q.serialize(data)
        for a in self.answers:
            a.serialize(data)
        data.seek(0)
        return data.read()
