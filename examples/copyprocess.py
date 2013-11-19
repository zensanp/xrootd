"""
Add a number of copy jobs and run them in parallel with a progress handler
--------------------------------------------------------------------------

Produces output similar to the following::

  id: 1, total: 4
  source: /tmp/spam
  target: /tmp/spam1
  processed: 20, total: 20
  end status: [SUCCESS] 
  id: 2, total: 4
  source: /tmp/spam
  target: root://localhost//tmp/spam2
  processed: 20, total: 20
  end status: [SUCCESS] 
  id: 3, total: 4
  source: root://localhost//tmp/spam
  target: /tmp/spam3
  processed: 20, total: 20
  end status: [SUCCESS] 
  id: 4, total: 4
  source: root://localhost//tmp/spam
  target: root://localhost//tmp/spam4
  processed: 20, total: 20
  end status: [SUCCESS] 

"""
from XRootD import client

class MyCopyProgressHandler(client.utils.CopyProgressHandler):
  def begin(self, id, total, source, target):
    print 'id: %d, total: %d' % (id, total)
    print 'source: %s' % source
    print 'target: %s' % target

  def end(self, status):
    print 'end status:', status

  def update(self, processed, total):
    print 'processed: %d, total: %d' % (processed, total)

process = client.CopyProcess()

# From local to local
process.add_job( '/tmp/spam', '/tmp/spam1' )
# From local to remote
process.add_job( '/tmp/spam', 'root://localhost//tmp/spam2' )
# From remote to local
process.add_job( 'root://localhost//tmp/spam', '/tmp/spam3' )
# From remote to remote
process.add_job( 'root://localhost//tmp/spam', 'root://localhost//tmp/spam4' )

handler = MyCopyProgressHandler()
process.prepare()
process.run(handler)
