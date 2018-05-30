# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse, abort
from common.response import Error

class Test(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('echo', type=str, required=True, location='args')

        args = parser.parse_args()

        return self.do(args)

    def post(self, api):
        parser = reqparse.RequestParser()
        parser.add_argument('echo', type=str, required=True, location='form')

        args = parser.parse_args()

        return self.do(args)

    def do(self, args):
        echo = args['echo']
        if echo == 'error':
            return Error(1, 'as you wish')

        return {
            'echo': args['echo'],
        }
