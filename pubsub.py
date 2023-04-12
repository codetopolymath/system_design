

class Broker(object):
    """
    Broker class
    """
    def __init__(self, name=''):
        self._name = name
        self._subscribers = [] # maintain subscriber list

    def attach(self, subscriber):
        """attach subscriber"""
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def detach(self, subscriber):
        """detach subscriber"""
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def route(self, msg, topic=''):
        """define route"""
        for subscriber in self._subscribers:
            if topic in subscriber.topic:
                subscriber.sub(msg)


class Publisher(object):
    """publisher class"""
    def __init__(self, name, broker):
        self._name = name
        self._broker = broker

    def pub(self, msg, topic=''):
        print('[Publisher: {}] topic: {}, message: {}'.format(self._name, topic, msg))
        self._broker.route(msg, topic)


class Subscriber(object):
    """subscriber class"""
    def __init__(self, name, broker, topic=None):
        self._name = name
        broker.attach(self)
        self._topic = [] if topic is None else topic

    def sub(self, msg):
        print('[Subscriber: {}] got message: {}'.format(self._name, msg))

    @property
    def topic(self):
        return self._topic


def main():
    # broker instance
    broker = Broker()

    # publishers
    p1 = Publisher('p1', broker)
    p2 = Publisher('p2', broker)

    # subscriber
    s1 = Subscriber('s1', broker, topic=['A'])
    s2 = Subscriber('s2', broker, topic=['A', 'B'])

    # publish to p1 and p2
    p1.pub('hello s1', topic='A')
    p2.pub('hello s2', topic='B')


if __name__ == '__main__':
    main()

    # expected output：
    # [Publisher: p1] topic: A, message: hello s1
    # [Subscriber: s1] got message: hello s1
    # [Subscriber: s2] got message: hello s1
    # [Publisher: p2] topic: B, message: hello s2
    # [Subscriber: s2] got message: hello s2

