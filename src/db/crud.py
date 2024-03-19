from src.db.models import DownloadRequest
from src.db.database import Session

session = Session()


async def create_download(
    url: str,
    data: object,
    ip_address: str,
):
    # create new row for download
    new_download = DownloadRequest(
        url=url,
        data=data,
        ip_address=ip_address,
    )
    session.add(new_download)
    session.commit()


async def read_download(url: str) -> DownloadRequest:
    # check download exists in DB or not
    download_request: DownloadRequest = (
        session.query(DownloadRequest).filter(DownloadRequest.url == url).first()
    )

    return download_request


async def delete_download(download: DownloadRequest):
    # delete download from database
    session.delete(download)
