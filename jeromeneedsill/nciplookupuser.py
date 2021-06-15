import xml.etree.ElementTree as ET
# not importing SubElement because we're going to use ET.SubElement
# in the fancy wrapper in ncip_lookup_user_xml_response_element_tree
from xml.etree.ElementTree import ElementTree, Element

def extract_user_identifier_from_ncip_lookup_user_XML(xmltext):
    root = ET.fromstring(xmltext)
    return root.findtext(
        '{http://www.niso.org/2008/ncip}LookupUser/'
        '{http://www.niso.org/2008/ncip}UserId/'
        '{http://www.niso.org/2008/ncip}UserIdentifierValue'
    )

# wrap SubElement constructor to add 'ns1:' prefix to all tags
# this is perhaps an overly enthusiastic attempt at
# being DRY (do not repeat yourself)
def SubElement(parent, tag):
    return ET.SubElement(parent, 'ns1:' + tag)

def SubElementWText(parent, tag, text):
    subelement = SubElement(parent, tag)
    subelement.text = text
    return subelement

def element_add_attributes(element, **attrkargs):
    element.attrib.update( { 'ns1:'+key: value
                                for key, value in attrkargs.items() } )

def SubElementWTextNAttr(parent, tag, text, **attrkargs):
    subelement = SubElementWText(parent, tag, text)
    element_add_attributes(subelement, **attrkargs)
    return subelement

def element_chain_all(superparent, *args, **attrkargs):
    """Recursively build a chain of SubElement, args is
    list of nested elements

    All elements constructed are returned as a tuple
    **attrkargs are added to the attrib dictionary of the last element"""
    assert len(args) != 0
    sub = SubElement(superparent, args[0])
    if len(args)==1:
        element_add_attributes(sub, **attrkargs)
        return (sub,)
    else:
        return (sub, ) + element_chain_all(sub, *args[1:], **attrkargs)

def element_chain(superparent, *args, **attrkargs):
    """Recursively build a chain of SubElement, args is
    list of nested elements

    Returns furthest element down the list"""
    # -1 meaning, last element
    last_element = element_chain_all(superparent, *args, **attrkargs)[-1]
    return last_element

def element_chain_all_text_terminal(superparent, text, *args, **attrkargs):
    """Recursively build a chain of SubElement, args is
    list of nested elements

    All elements constructed are returned as a tuple
    The text argument is added as a .text property to the deepest element
    """
    result = element_chain_all(superparent, *args, **attrkargs)
    result[-1].text = text
    return result

def element_chain_text_terminal(superparent, text, *args, **attrkargs):
    """Recursively build a chain of SubElement, args is
    list of nested elements

    Returns furthest element down the list
    The text argument is added as a .text property to this deepest element
    """
    return element_chain_all_text_terminal(
        superparent, text, *args, **attrkargs)[-1]

def ncip_lookup_user_xml_response_add_name_fields(
        uof, # UserOptionalFields element
        given_name=None, surname=None, unstructured_name=None):
    # first prevent the wrong combination of name fields
    if (given_name!=None or surname!=None) and unstructured_name!=None:
        raise Exception(
            """only allowed is given_name and/or surname, or """
            """unstructed_name or neither, not both""")
    # then, if any of them, get the outer elements started
    elif given_name != None or surname != None:
        spun = element_chain(
            uof,
            'NameInformation',
            'PersonalNameInformation',
            'StructuredPersonalUserName')
        if given_name != None:
            SubElementWText(spun, 'GivenName', given_name)
        if surname != None:
            SubElementWText(spun, 'Surname', surname)
    elif unstructured_name!=None:
        element_chain_text_terminal(
            uof, unstructured_name,
            'NameInformation', 'PersonalNameInformation',
            'UnstructuredPersonalUserName')
    else:
        pass # do nothing if no name present

def ncip_lookup_user_xml_response_add_user_privilege(
        uof, # UserOptionalFields element
        privilege_set, # hash with specific privileges
):
    if any( x not in privilege_set
            for x in ('AgencyId', 'AgencyUserPrivilegeType') ):
        raise Exception(
            "AgencyId/AgencyUserPrivilegeType is not yet established")

    user_priv_elem, ai = element_chain_all_text_terminal(
        uof, privilege_set['AgencyId'], # text
        'UserPrivilege', 'AgencyId', # tags
        Scheme="NCIP Unique Agency Id") # attrib for last element, ai

    SubElementWTextNAttr(
        user_priv_elem,
        'AgencyUserPrivilegeType', # tag
        privilege_set['AgencyUserPrivilegeType'], # text
        Scheme=privilege_set['privilege_type_scheme'] # attributes
    )
    if all( x in privilege_set
            for x in ('UserPrivilegeStatusType',
                      'privilege_status_type_scheme') ):
        upst = element_chain_text_terminal(
            user_priv_elem,
            privilege_set['UserPrivilegeStatusType'], # text
            'UserPrivilegeStatus', 'UserPrivilegeStatusType', # tags
            Scheme=privilege_set['privilege_status_type_scheme']) # attributes

def ncip_lookup_user_xml_response_add_user_id_element(
        uof, identifier_value,
        identifier_type=None, identifier_type_schema=None):
    user_id_element = SubElement(uof, 'UserId')
    if identifier_type != None:
        # prepare empty or populated dictionary for **kargs use below
        useridenttypekargs = {}
        if identifier_type_schema != None:
            useridenttypekargs['Scheme'] = identifier_type_schema
        SubElementWTextNAttr(
            user_id_element,
            'UserIdentifierType', # tag
            identifier_type, # text
            **useridenttypekargs)
    SubElementWText(user_id_element, 'UserIdentifierValue', identifier_value)

def create_ncip_message_root_element():
    root = Element('ns1:NCIPMessage')
    root.set('xmlns:ns1', "http://www.niso.org/2008/ncip")
    root.set(
        'ns1:version',
        "http://www.niso.org/schemas/ncip/v2_0/imp1/xsd/ncip_v2_0.xsd")
    return root

def create_ncip_lookup_user_response_element_w_response_header(
        root, agency):
    lur, rh = element_chain_all(root, 'LookupUserResponse', 'ResponseHeader')

    element_chain_all_text_terminal(
        rh, agency, 'FromAgencyId', 'AgencyId')
    element_chain_all_text_terminal(
        rh, agency, 'ToAgencyId', 'AgencyId')

    return lur

def ncip_lookup_user_xml_response_element_tree(
        agency, user_identifier,
        given_name=None, surname=None, unstructured_name=None,
        email=None, email_role_type='Home',
        language=None,
        user_privileges=None,
        primary_key=None,
        primary_key_schema=None,
        barcode=None,
        barcode_key_schema=None,
):
    """only unstructured_name, or one or both of given_name/surname, or
    none of them may be set. In terms of NCIP, results in
    UnstructuredPersonalUserName or StructuredPersonalUserName
    """
    root = create_ncip_message_root_element()
    lur = create_ncip_lookup_user_response_element_w_response_header(
        root, agency)

    element_chain_text_terminal(
        lur, user_identifier, 'UserId', 'UserIdentifierValue')

    # check for any of the many fields covered by UserOptionalFields
    # (name, barcode, email) are in use
    if any( x!=None
            for x in (given_name, surname, unstructured_name,
                      email, language, user_privileges,
                      primary_key, barcode) ):
        uof = SubElement(lur, 'UserOptionalFields')

        # handle the name fields specifically
        ncip_lookup_user_xml_response_add_name_fields(
            uof,
            given_name=given_name, surname=surname,
            unstructured_name=unstructured_name)

        if email != None:
            uai = element_chain_all_text_terminal(
                uof, email_role_type,
                'UserAddressInformation',
                'UserAddressRoleType')[0] # save only first returned element
            ea, eat = element_chain_all_text_terminal(
                uai, 'mailto', # text
                'ElectronicAddress', 'ElectronicAddressType', # tags
                Scheme="NCIP electronic Address Type Scheme") # eat attributes
            email_element = SubElementWText(
                ea, 'ElectronicAddressData', email)

        if language != None:
            SubElementWText(uof, 'UserLanguage', language)

        if user_privileges != None:
            for privilege_set in user_privileges:
                ncip_lookup_user_xml_response_add_user_privilege(
                    uof, privilege_set)

        if primary_key != None:
            ncip_lookup_user_xml_response_add_user_id_element(
                uof, primary_key,
                identifier_type='Primary Key',
                identifier_type_schema=primary_key_schema)

        if barcode != None:
            ncip_lookup_user_xml_response_add_user_id_element(
                uof, barcode,
                identifier_type='Barcode',
                identifier_type_schema=barcode_key_schema)

        return ElementTree(element=root)

def ncip_lookup_user_xml_response_element_tree_as_string(
        agency, user_identifier, **kargs):
    return ET.tostring(
        ncip_lookup_user_xml_response_element_tree(
            agency, user_identifier, **kargs).getroot() )

def ncip_lookup_user_response_error_element_tree(
        agency, problem_type, problem_detail):
    root = create_ncip_message_root_element()
    lur = create_ncip_lookup_user_response_element_w_response_header(
        root, agency)

    prob = element_chain_all_text_terminal(
        lur, problem_type,
        'Problem', 'ProblemType')[0] # save only first returned element
    SubElementWText(
        prob, 'ProblemDetail', problem_detail)

    return ElementTree(element=root)

def ncip_lookup_user_response_error_element_tree_as_string(
        agency, problem_type, problem_detail):
    return ET.tostring(
        ncip_lookup_user_response_error_element_tree(
            agency, problem_type, problem_detail).getroot() )

# for testing this module on its own
if __name__ == "__main__":
    #print( extract_user_identifier_from_ncip_lookup_user_XML(
    """<?xml version="1.0" encoding="UTF-8"?>
<NCIPMessage version="http://www.niso.org/schemas/ncip/v2_0/ncip_v2_0.xsd" xmlns="http://www.niso.org/2008/ncip" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <LookupUser>
    <InitiationHeader>
      <ToAgencyId>
        <AgencyId>MWUC</AgencyId>
      </ToAgencyId>
      <ApplicationProfileType>RELAIS</ApplicationProfileType>
    </InitiationHeader>
    <UserId>
      <UserIdentifierValue>12345678</UserIdentifierValue>
    </UserId>
    <UserElementType>Name Information</UserElementType>
    <UserElementType>User Address Information</UserElementType>
    <UserElementType>User Language</UserElementType>
    <UserElementType>User Privilege</UserElementType>
    <UserElementType>User Id</UserElementType>
  </LookupUser>
</NCIPMessage>
"""
    #    ) )

    from sys import stdout
    blah = ncip_lookup_user_xml_response_element_tree(
        agency='TEST',
        user_identifier='TESTUSER',
        given_name='Testser',
        surname='Testkins',
        #unstructured_name='blah',
        email='test@locahost',
        language='en',
        user_privileges=(
            {'AgencyId': 'Agency full name',
             'AgencyUserPrivilegeType': 'STATUS',
             'privilege_type_scheme':
             'University of Blah User Privilege Type Academic Scheme',
             'UserPrivilegeStatusType': 'ACTIVE',
             'privilege_status_type_scheme':
             "University of Blah User Privilege Status Type Scheme"
            },),
        primary_key='8765432',
        primary_key_schema="University of Blah User Identifier Type Scheme",
        barcode='8765432',
        barcode_key_schema="University of Blah User Identifier Type Scheme",
        )
    blah.write(
        stdout.buffer,
        xml_declaration=True,
        encoding="UTF-8",
        )
    #ET.dump(blah)
    #print(ncip_lookup_user_response_error_element_tree_as_string
    #      ('TESTINST', 'Unknown User',
    #       'NCIP LookUpUser Processing Error Scheme').decode('UTF-8'))
