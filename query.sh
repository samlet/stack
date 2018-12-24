#!/bin/bash
curl -XPOST localhost:5000/parse -d '{"q":"Allô", "project":"french"}'
