#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 10:51:45 2020

@author: trabdlkarim
"""


from datetime import datetime
from datetime import timezone
import time


delta = datetime.now(timezone.utc)
print(delta.timestamp())
lt = delta.timestamp()-(3600*3)

t =time.gmtime(lt)
print(lt)
print(delta)
print(t)