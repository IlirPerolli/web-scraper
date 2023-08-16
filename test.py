from Jobs.Kastori import Kastori

tender_url = "http://e-tenderi.test/api/tenders"
job_url = "http://e-tenderi.test/api/jobs"

kastori = Kastori()
print (kastori.get_data())