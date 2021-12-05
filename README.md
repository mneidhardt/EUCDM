# EUCDM
Stuff to help manage the beast.

Currently, this can create JSON Schemas for one of the H* or I* messages (or "columns" as they are called in EUCDM)..

To create JSON Schema for one of the messages, do this:
Have a CSV file ready, containing one row per Data Element, with DE number, the column presence (mandatory etc.) and the cardinality for each of the levels.
Have another CSV ready, also containing one row per Data Element with both the number, name and format for each DE.
The precise contents of these 2 CVS files will be described here in due time.

Then just create a serialised graph of the message ("column") you need a schema for:
>python3 extractSerialisedGraph.py data/DEColumnPresenceCardinality.csv > data/serialisedgraph.txt

And then create the JSON Schema based on the serialised graph:
>python3 buildjsonschema.py data/serialisedgraph.txt data/EUCDM6_DataElements.CSV


