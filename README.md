# DICOM RENAMER

Designed on behalf of Québec Mille Familles (Q1K) to prepare their magentic resonance imaging data (MRI) for ingestion into the CBIG repository.

The Programme links the MRI data with the associated candidate identifier in the CBIG API. It renames the MRI archives names and the patient name of each DICOM file. Each archive can contain up to 5000 files of up to 1 MB, so, an automation programme with a logging system and resume-on-fail functionality was needed.

This programme was borne out of a collaboration at the Montreal Neurological institute: the C.Tardif Lab and LORIS (Longitudinal Online Research and Imaging System). 

Quebec Mille Familles: https://q1k.ca/en/
Tardif Lab: https://www.tardiflab.com/team
Clinical Biospecimen Imaging and Genetics: https://cbigr-open.loris.ca/
