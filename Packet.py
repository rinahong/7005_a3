class Packet:
    def __init__(self, packet_type, seq_num = '', ack_num = '', data = ''):
      self.packet_type = packet_type
      self.seq_num = seq_num
      self.ack_num = ack_num
      self.data = data
