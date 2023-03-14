"""Constant package."""
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

##
# State Machines
# Vendor: DRAFT --> CERTIFIED
# VSP: DRAFT --> UPLOADED --> VALIDATED --> COMMITED --> CERTIFIED
##

##
# States
##
DRAFT = "Draft"
CERTIFIED = "Certified"
COMMITED = "Commited"
UPLOADED = "Uploaded"
VALIDATED = "Validated"
APPROVED = "Approved"
UNDER_CERTIFICATION = "Certification in progress"
CHECKED_IN = "Checked In"
SUBMITTED = "Submitted"
DISTRIBUTED = "Distributed"
ARCHIVED = "ARCHIVED"
##
# Actions
##
CERTIFY = "Certify"
COMMIT = "Commit"
CREATE_PACKAGE = "Create_Package"
SUBMIT = "Submit"
ARCHIVE = "ARCHIVE"
SUBMIT_FOR_TESTING = "certificationRequest"
CHECKOUT = "checkout"
UNDOCHECKOUT = "UNDOCHECKOUT"
CHECKIN = "checkin"
APPROVE = "approve"
DISTRIBUTE = "PROD/activate"
TOSCA = "toscaModel"
DISTRIBUTION = "distribution"
START_CERTIFICATION = "startCertification"
NOT_CERTIFIED_CHECKOUT = "NOT_CERTIFIED_CHECKOUT"
NOT_CERTIFIED_CHECKIN = "NOT_CERTIFIED_CHECKIN"
READY_FOR_CERTIFICATION = "READY_FOR_CERTIFICATION"
CERTIFICATION_IN_PROGRESS = "CERTIFICATION_IN_PROGRESS"
DISTRIBUTION_APPROVED = "DISTRIBUTION_APPROVED"
DISTRIBUTION_NOT_APPROVED = "DISTRIBUTION_NOT_APPROVED"
SDC_DISTRIBUTED = "DISTRIBUTED"
##
# Distribution States
##
DOWNLOAD_OK = "DOWNLOAD_OK"
