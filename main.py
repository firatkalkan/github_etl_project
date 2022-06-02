from ApiClass import ApiClass
from datetime import date
import logging
import os

if __name__ == '__main__':

    slogDir = "logs/"
    if not os.path.exists(slogDir):
        os.makedirs(slogDir)

    today = date.today()
    dateStr = today.strftime("%d_%b_%Y")
    sDailyLog = slogDir + dateStr + ".log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s : %(levelname)s : %(message)s',
        handlers=[
            logging.FileHandler(sDailyLog),
            logging.StreamHandler()
        ]
    )

    sUserName = input("Github user name: ")
    sRepoName = input("Github repo name: ")

    # sUserName = "hyle-team"
    # sRepoName = "zano_ui"

    sProcess = input(" Press 'A' for Avarage time between pull requests"
                     "\n Press 'T' for total number of events grouped by the event type for "
                     + sUserName + "/" + sRepoName + " repository \n"
                     )

    apiCall = ApiClass(sUserName, sRepoName, logging)


    if sProcess == "A":
        logging.info("Avarage time between pull requests for " + sUserName + "/" + sRepoName + "repository is calculating ...")
        apiCall.avaragePullReqTime()
        logging.info("Succesfully Finished")

    elif sProcess == "T":
        offset = input("Do you want to set offset (or leave empty): ")
        logging.warning("OFFSET VALUE: " + offset)
        logging.info("Total number of events grouped by the event type " + sUserName + "/" + sRepoName + "repository is calculating ...")
        apiCall.totalGroupEvent(offset)
        logging.info("Succesfully Finished")

    else:
        logging.error("Invalid process")



