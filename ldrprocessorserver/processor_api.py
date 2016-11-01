from flask import jsonify, Blueprint, send_file, make_response
from flask_restful import Resource, Api, reqparse
from io import BytesIO
from os import listdir
from os.path import join, exists
from werkzeug.utils import secure_filename
from re import compile as regex_compile
from xml.etree import ElementTree as ET
from sys import stderr
from uchicagoldrapicore.responses.apiresponse import APIResponse
from uchicagoldrapicore.responses.apiresponse import APIResponse
from uchicagoldrapicore.lib.apiexceptionhandler import APIExceptionHandler

from uchicagoldrtoolsuite.bit_level.lib.readers.filesystemarchivereader import FileSystemArchiveReader
from uchicagoldrtoolsuite.bit_level.lib.ldritems.ldrpath import LDRPath

_ALPHANUM_PATTERN = regex_compile("^[a-zA-Z0-9]+$")
_NUMERIC_PATTERN = regex_compile("^[0-9]+$")
_EXCEPTION_HANDLER = APIExceptionHandler()

# Create our app, hook the API to it, and add our resources

BP = Blueprint("ldrprocessorserverapi", __name__)
API = Api(BP)

def createPremisObject(object_path):
    """
    http://www.loc.gov/premis/v3 is the premis namespace url
    """
    if exists(join(object_path, "premis.xml")):
        return ET.parse(join(object_path, "premis.xml")).getroot()
    else:
        return "none"

def get_premis_mimetype(premis_file_data):
    root = premis_file_data
    return root.find("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}objectCharacteristics/{http://www.loc.gov/premis/v3}format/{http://www.loc.gov/premis/v3}formatDesignation/{http://www.loc.gov/premis/v3}formatName").text



class GetAContentItem(Resource):
    """
    fill_in_please
    """

    def get(self, arkid, premisid):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            premis_record = createPremisObject(path_to_object)
            content_item = path_to_object+"/content.file"
        else:
            premis_record = "{}/premis.xml does not exist".format(path_to_object)
            content_itm = "{}/content.file does not exist".format(path_to_object)
        try:
            mimetype = get_premis_mimetype(premis_record)
            file_extension = mimetype.split('/')[1]

            resp = send_file(content_item, as_attachment=True, attachment_filename=premisid+"." + file_extension, mimetype=get_premis_mimetype(premis_record), )


            return resp
        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())

class GetAPremisItem(Resource):
    """
    fill_in_please
    """

    def get(self, arkid, premisid):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            premis_record = createPremisObject(path_to_object)
            content_item = path_to_object+"/premis.xml"
        else:
            premis_record = "{}/premis.xml does not exist".format(path_to_object)
            content_itm = "{}/content.file does not exist".format(path_to_object)
        try:
            mime = "application/xml"
            file_extension = '.xml'

            resp = send_file(content_item, mimetype=mime)
            return resp
        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())

class GetTechMetadataList(Resource):
    """
    fill_in_please
    """

    def get(self, arkid, premisid):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            content_item = path_to_object+"/premis.xml"
        else:
            content_item = "{}/content.file does not exist".format(path_to_object)
        try:
            techmd_list = [x for x in listdir(path_to_object) if x.endswith('.xml') and 'premis' not in x]
            output = {}
            for i in range(len(techmd_list)):
                output[str(i)] = {"label": techmd_list[i].split('.xml')[0], "loc":"/" + arkid + "/" + premisid + "/techmds/" + str(i)}



            resp = APIResponse("success",
                               data={"technical_metadata": output})
            return jsonify(resp.dictify())


        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())

class GetASpecificTechnicalMetadata(Resource):
    def get(self, arkid, premisid, numbered_request):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            content_item = path_to_object+"/premis.xml"
        else:
            content_item = "{}/content.file does not exist".format(path_to_object)
        try:
            techmd_list = [x for x in listdir(path_to_object) if x.endswith('.xml') and 'premis' not in x]
            content_item = "{}/{}".format(path_to_object, techmd_list[int(numbered_request)])
            resp = send_file(content_item, mimetype="application/xml")
            return resp

            return jsonify(resp.dictify())


        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())



class GetPresformsList(Resource):
    """
    fill_in_please
    """

    def get(self, arkid, premisid):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            premis_record = createPremisObject(path_to_object)
            presform_list_ids = premis_record.findall("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}relationship/{http://www.loc.gov/premis/v3}relatedObjectIdentification/{http://www.loc.gov/premis/v3}relatedObjectIdentifierValue")
        else:
            premis_record = "{}/premis.xml does not exist".format(path_to_object)
            content_itm = "{}/content.file does not exist".format(path_to_object)
        try:
            output = {}
            if len(presform_list_ids) == 0:
                output['value'] = "no presforms for this object"
                resp = APIResponse("success",
                               data={"presforms": output})
            else:
                output['presforms'] = []
                for n in presform_list_ids:
                    n_text = "/" + arkid + "/" + n.text + "/content"
                    output['prsforms'].append({"loc":n_text})
            return jsonify(resp.dictify())
        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())

class GetASpecificPresform(Resource):
    def get(self, arkid, premisid, numbered_request):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            content_item = path_to_object+"/premis.xml"
        else:
            content_item = "{}/content.file does not exist".format(path_to_object)
        try:
            output = "testing"
            for i in range(len(techmd_list)):
                output[str(i)] = "https://y2.lib.uchicago.edu/processor/" + arkid + "/" + premisid + "/techmds/" + str(i)
            resp = APIResponse("success",
                               data={"presform": output})
            return jsonify(resp.dictify())


        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())

class ConvenienceToGetLastPresformOrContent(Resource):
    def get(self, arkid, premisid):
        """
        Get the whole record
        """
        n = 2
        arkid_split = [arkid[i:i+n] for i in range(0, len(arkid), n)]
        premisid_split =[premisid[i:i+n] for i in range(0, len(premisid), n)]
        path_to_object = join("/data/repository/longTermStorage", "/".join(arkid_split), "arf/pairtree_root", "/".join(premisid_split), "arf")
        if exists(path_to_object):
            premis_record = createPremisObject(path_to_object)
            content_item = path_to_object + "/content.file"
            presform_list_ids = premis_record.findall("{http://www.loc.gov/premis/v3}object/{http://www.loc.gov/premis/v3}relationship/{http://www.loc.gov/premis/v3}relatedObjectIdentification/{http://www.loc.gov/premis/v3}relatedObjectIdentifierValue")
        else:
            premis_record = "{}/premis.xml does not exist".format(path_to_object)
            content_item = "{}/content.file does not exist".format(path_to_object)
        try:
            output = {}
            if len(presform_list_ids) == 0:
                mime = get_premis_mimetype(premis_record)
                resp = send_file(content_item, mimetype=mime, as_attachment=True, attachment_filename=premisid)

                return resp
            else:
                id_to_fetch + presform_id_list[-1]
                id_to_fetch_split = [id_to_fetch[i:i+n] for i in range(0, len(id_to_fetch), n)]
                presform_item = join("/data/repository/longTermStorage", '/'.join(arkid_split), '/'.join(id_to_fetch_split), '/content.file')
                presform_item_premis_record = join("/data/repository/longTermStorage", '/'.join(arkid_split), '/'.join(id_to_fetch_split), '/premis.xml')
                presform_item_presmis_root = get_premis_mimetype(createPremisObject(presform_item_premis_record))
                presform_item_mime = get_premis_mimetype(presform_item_premis_root)
                resp = send_file(presform_item, mimetype=presform_item_mime, as_attachment=True, attachment_filename=id_to_fetch)





            return jsonify(resp.dictify())
        except Exception as e:
            return jsonify(_EXCEPTION_HANDLER.handle(e).dictify())





# Record manipulation endpoints
API.add_resource(GetAContentItem, "/<string:arkid>/<string:premisid>/content")
API.add_resource(GetAPremisItem, "/<string:arkid>/<string:premisid>/premis")
API.add_resource(GetTechMetadataList, "/<string:arkid>/<string:premisid>/techmds")
API.add_resource(GetASpecificTechnicalMetadata, "/<string:arkid>/<string:premisid>/techmds/<int:numbered_request>")
API.add_resource(GetPresformsList, "/<string:arkid>/<string:premisid>/presforms")
API.add_resource(GetASpecificPresform, "/<string:arkid>/<string:premisid>/presforms/<int:numbered_request>")
API.add_resource(ConvenienceToGetLastPresformOrContent, "/<string:arkid>/<string:premisid>/presform")


def only_alphanumeric(n_item):
    """
    fill_in_please
    """
    if _ALPHANUM_PATTERN.match(n_item):
        return True
    return False


def retrieve_record(identifier):
    """
    fill_in_please
    """
    identifier = secure_filename(identifier)
    if not only_alphanumeric(identifier):
        raise ValueError("Record identifiers must be alphanumeric.")
    r_test = "test"
    return r_test

