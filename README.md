dadvisor
========

docker monitoring tool. this is a __proof of concept__ demonstrating the ease at which you can monitor containers from their host machines.
monitors cpu and memory now.
can be expanded to network stats, etc. anything that isn't application specific

__based on__ <a href ='http://jpetazzo.github.io/2013/10/08/docker-containers-metrics/'>this article</a>

# Future

integrate this onto mesos-slaves to monitor container performance metrics and provide a clean way for theseus (or any container management framework
to access performance data about containers)
