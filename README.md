# cycleGAN-pws
CycleGAN for converting faces of PWS (Port-Wine Stain Birthmarks) to clear faces and vice versa
Abstract link: [here](https://www.aslms.org/annual-conference-2024/for-attendees/program/program-at-a-glance)


## Data requirements
* 7028 photos of human faces (clear faces) taken from Kaggle's dataset [here](https://www.kaggle.com/datasets/ashwingupta3012/human-faces)
* 300 photos of human pws faces scraped and pre-processed from Google Images using the script `web_scraping/one_off_data_generator/scrape_google_images.py`, combined with the internal dataset of PWS photos from the clinic

## GPU Requirements
I've used the Kaggle's GPU for training the model. The GPU is NVIDIA Tesla P100-PCIE-16GB. The training time for 200 epochs is around 2 hours.


### Self-notes
* Since running on M2 macbook, I was required to set up trensorflow-metal package. To run the python w. tf2 support on M2 chip run (on my PC): `source ~/tensorflow-metal/bin/activate`