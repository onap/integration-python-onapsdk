"""Global settings module."""
#   Copyright 2022 Orange, Deutsche Telekom AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


######################
#                    #
# ONAP SERVICES URLS #
#                    #
######################

## API
AAI_URL                     = "https://aai.api.sparky.simpledemo.onap.org:30233"
AAI_API_VERSION             = "v27"
AAI_AUTH                    = "Basic QUFJOkFBSQ=="
AAI_BULK_CHUNK              = 30
CDS_URL                     = "http://portal.api.simpledemo.onap.org:30449"  # NOSONAR
CDS_AUTH                    = ("ccsdkapps", "ccsdkapps")
CPS_URL                     = "http://portal.api.simpledemo.onap.org:8080"  # NOSONAR
CPS_AUTH                    = ("cpsuser", "cpsr0cks!")
CPS_VERSION                 = "v2"
MSB_URL                     = "https://msb.api.simpledemo.onap.org:30283"
K8SPLUGIN_URL               = "http://k8splugin.api.simpledemo.onap.org:30455"  # NOSONAR
SDC_BE_URL                  = "https://sdc.api.be.simpledemo.onap.org:30204"
SDC_FE_URL                  = "https://sdc.api.fe.simpledemo.onap.org:30207"
SDC_AUTH                    = "Basic YWFpOktwOGJKNFNYc3pNMFdYbGhhazNlSGxjc2UyZ0F3ODR2YW9HR21KdlV5MlU="  # pylint: disable=line-too-long
SDNC_URL                    = "https://sdnc.api.simpledemo.onap.org:30267"
SDNC_AUTH                   = "Basic YWRtaW46S3A4Yko0U1hzek0wV1hsaGFrM2VIbGNzZTJnQXc4NHZhb0dHbUp2VXkyVQ=="  # pylint: disable=line-too-long
SO_CATALOG_DB_ADAPTER_URL   = "http://so-catalog-db-adapter:8082"  # NOSONAR
SO_URL                      = "http://so.api.simpledemo.onap.org:30277"  # NOSONAR
SO_API_VERSION              = "v7"
SO_AUTH                     = "Basic SW5mcmFQb3J0YWxDbGllbnQ6cGFzc3dvcmQxJA=="
SO_CAT_DB_AUTH              = "Basic YnBlbDpwYXNzd29yZDEk"
VID_URL                     = "https://vid.api.simpledemo.onap.org:30200"
VID_API_VERSION             = "/vid"
CLAMP_URL                   = "https://clamp.api.simpledemo.onap.org:30258"
CLAMP_AUTH                  = "Basic ZGVtb0BwZW9wbGUub3NhYWYub3JnOmRlbW8xMjM0NTYh"
VES_URL                     = "http://ves.api.simpledemo.onap.org:30417"  # NOSONAR
DMAAP_URL                   = "http://dmaap.api.simpledemo.onap.org:3904"  # NOSONAR
NBI_URL                     = "https://nbi.api.simpledemo.onap.org:30274"
NBI_API_VERSION             = "/nbi/api/v4"
DCAEMOD_URL                 = ""
HOLMES_URL                  = "https://aai.api.sparky.simpledemo.onap.org:30293"
POLICY_URL                  = ""

## GUI
AAI_GUI_URL = "https://aai.api.sparky.simpledemo.onap.org:30220"
AAI_GUI_SERVICE = f"{AAI_GUI_URL}/services/aai/webapp/index.html#/browse"
CDS_GUI_SERVICE = f"{CDS_URL}/"
SO_MONITOR_GUI_SERVICE = f"{SO_URL}/"
SDC_GUI_SERVICE = f"{SDC_FE_URL}/sdc1/portal"
SDNC_DG_GUI_SERVICE = f"{SDNC_URL}/nifi/"
SDNC_ODL_GUI_SERVICE = f"{SDNC_URL}/odlux/index.html"

DCAEMOD_GUI_SERVICE = f"{DCAEMOD_URL}/"
HOLMES_GUI_SERVICE = f"{HOLMES_URL}/iui/holmes/default.html"
POLICY_GUI_SERVICE = f"{POLICY_URL}/onap/login.html"
POLICY_CLAMP_GUI_SERVICE = f"{CLAMP_URL}/"

# VID OBJECTS DEFAULT VALUES
PROJECT = "Onapsdk_project"
LOB = "Onapsdk_lob"
PLATFORM = "Onapsdk_platform"

DEFAULT_REQUEST_TIMEOUT = 60
