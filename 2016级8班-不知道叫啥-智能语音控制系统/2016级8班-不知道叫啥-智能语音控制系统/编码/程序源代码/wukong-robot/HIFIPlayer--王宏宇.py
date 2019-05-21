# -*- coding: utf-8-*-
import paramiko
from robot import logging
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)

ip='192.168.137.102'
port = 22
username = 'volumio'
password = 'Darkness1997'

class HiFiPlayer(object):
    
    def __init__(self, plugin):
        super(HiFiPlayer, self).__init__()
        self.plugin = plugin
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    def play(self):
        logger.debug('MusicPlayer play')
        self.ssh.connect(ip, port,username, password)
        cmd='volumio play'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        
    def next(self):
        logger.debug('MusicPlayer next')
        cmd='volumio next'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
    
    def prev(self):
        logger.debug('MusicPlayer prev')
        cmd='volumio previous'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

    def stop(self):
        logger.debug('MusicPlayer stop')        

    def turnUp(self):
        cmd='volumio volume plus'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

    def turnDown(self):
        cmd='volumio volume minus'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        
    def stop(self):
        logger.debug('MusicPlayer stop')
        cmd='volumio stop'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        self.ssh.close()
        
class Plugin(AbstractPlugin):
    
    SLUG = "HIFIPlayer"
    IS_IMMERSIVE = True
        
    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None
    
    def init_music_player(self):
        return HiFiPlayer(self)
        
    def handle(self, text, parsed):
        if not self.player:
            self.player = self.init_music_player()
        if self.nlu.hasIntent(parsed, 'MUSICRANK'):
            self.player.play()
        elif self.nlu.hasIntent(parsed, 'CHANGE_TO_NEXT'):
            self.say('下一首歌')
            self.player.next()
        elif self.nlu.hasIntent(parsed, 'CHANGE_TO_LAST'):
            self.say('上一首歌')
            self.player.prev()
        elif self.nlu.hasIntent(parsed, 'CHANGE_VOL'):
            word = self.nlu.getSlotWords(parsed, 'CHANGE_VOL', 'user_vd')[0]
            if word == '--LOUDER--':
                self.say('大声一点')
                self.player.turnUp()
            else:
                self.say('小声一点')
                self.player.turnDown()
        elif self.nlu.hasIntent(parsed, 'CLOSE_MUSIC') or self.nlu.hasIntent(parsed, 'PAUSE'):        
            self.player.stop()
            self.clearImmersive()  # 去掉沉浸式
            self.say('退出播放')
        else:
            self.say('没听懂你的意思呢，要停止播放，请说停止播放')
            self.player.play()


    def isValidImmersive(self, text, parsed):
        """ 判断是否当前音乐模式下的控制指令 """
        return any(self.nlu.hasIntent(parsed, intent) for intent in ['CHANGE_TO_LAST', 'CHANGE_TO_NEXT', 'CHANGE_VOL', 'CLOSE_MUSIC', 'PAUSE'])

    def isValid(self, text, parsed):
        return any(word in text for word in ["高品质音乐"])
        
        
