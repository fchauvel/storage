#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

FROM python:3.4-slim

LABEL maintainer "franck.chauvel@sintef.no"

# Update the dist and install needed tools
RUN apt-get -qq update

# Fetch, build and install sensapp-storage
COPY . storage
WORKDIR storage
RUN pip install -r requirements.txt
RUN pip install .

# Run sensapp-storage
CMD ["sensapp-storage", "-q", "task-queue", "-n", "SENSAPP_TASK"]


