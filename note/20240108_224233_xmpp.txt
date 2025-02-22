.note #xmpp
1.XMPP 公开群聊或频道搜索引擎
https://search.jabber.network/
> 符合条件的群聊会搜索到，有的管理员也会拒绝自己的服务器被搜索。
> 搜索少于3个代码点会忽略，不支持中文，不区分大小写，不支持搜索群聊语言配置。
> 配置公开群聊时，最好在描述里边包含Chinese之类的关键词，最好是中文英文都有。中文是给了解中文的人看的，英文是为了搜索方便。
> 正确的语言设置是为了方便让别人知道群聊主要说什么语言。中文：zh。英文：en。

2.Matrix 对 XMPP 的桥接服务
#room#matrix.domain.tld@matrix.org

3.OMEMO 多端消息和对象加密 
https://conversations.im/omemo/
> 有的客户端支持多种加密，目前推荐使用OMEMO加密。推荐使用这些客户端Conversations、monocles chat、Cheogram、Gajim、Dino、Converse、Movim、Monal、Siskin、Profanity、Poezio

4.跟踪 XMPP 客户端中 OMEMO 集成的进度
https://omemo.top/
> 不是所有客户端都支持OMEMO加密，选择适合自己的。客户端推荐顺序，建议搭配使用
> ①Conversations/Cheogram/monocles chat  ②aTalk/jTalk/BombusMod  ③yaxim/Xabber/Stork IM
> 第①组优先推荐Conversations，功能由少到多，但不如Conversations稳定。第②组优先推荐aTalk，功能由少到多，卡顿。第③组功能简单，可以补充前面都没有的功能。
> ①Gajim  ②Dino  ③Psi+
> 优先推荐Gajim，功能满足日常需求，Dino支持语音视频通话，Psi+可以补充前面没有的功能。
> ①Converse ②Movim ③Xabber Web
> Converse适用于大多数服务器，功能丰富。Movim适用于比较新的服务器版本，功能丰富。Xabber Web功能不算多，有特色功能。
> 远离苹果。Monal、Siskin，各有优缺点。

5.XMPP 官方网站
https://xmpp.org/
> 关于XMPP的更多信息。

XMPP 小工具 .note #xmppt
XMPP 服务器列表汇总 .note #xmppl
XMPP Android 客户端 .note #xmppa
XMPP Web 客户端 .note #xmppw
XMPP 其他客户端 .note #xmppo
XMPP 提供者 .note #xmppp


.note #xmppt
XMPP 小工具
①XMPP 状态检查器 
https://connect.xmpp.net/
> 帮助你检查服务器的连接状态。

②XMPP 服务器的 MITM 检测和监控
https://certwatch.xmpp.net/
> 帮助你检查XMPP服务器的TLS设置。

③XMPP 账号导出器
https://migrate.modernxmpp.org/
> 目前仅支持联系人列表（花名册）、个人资料信息（vCard）
下边这个是suchat.org管理员自己搭建的。
https://www.suchat.org/exportador/

④XMPP 合规性测试
https://compliance.conversations.im/
> 不更新维护了，未来会关闭，仅参考。

⑤XMPP TLS 加密配置测试
https://cryptcheck.fr/
> 以yax.im为例，就是：https://cryptcheck.fr/xmpp/yax.im
> 这个评分不要怕，E算正常，F稍微有点差。yax.im管理员升级后，没有淘汰使用旧设备的用户。

.note #xmppl
XMPP 服务器列表汇总
①https://providers.xmpp.net/
> 可能对新用户友好，对服务器进行了等级划分，注册相关，是否免费，是否专业托管、绿色托管，能否重设密码，有一些不合理的划分，选择一个适合自己的。服务器能用，一些信息不准确。
②https://jabberworld.info/servers/
> 记录服务器软件及其版本、在线时长。部分服务器不能用，部分信息不准确。
③https://compliance.conversations.im/old/
> 旧版合规性测试，有些服务器不能用一些结果不准确，当初按照这个404.city在第一，很多人按照顺序注册。后来换成新版的随机推荐5个。部分服务器不能用，部分结果不准确。
④https://xmpp.love/
> C2S是客户端到服务器的连接， S2S是服务器到服务器的连接，INBAND表示用户可以从客户端注册。部分服务器不能用，部分结果不准确。
⑤https://the-federation.info/protocol/20/
> 显示服务器软件及其版本、位置和是否开放注册等其他信息。部分服务器不能用，部分信息不准确。
⑥https://xmpp.404.city/
> 显示服务器开始运营时间等其他信息。当初404.city管理员的服务器没被一些列表接受，才有了这个。部分服务器不能用，部分信息不准确。
⑦https://list.jabber.at/
> 显示服务器位置和开始运营时间等其他信息。部分服务器不能用，部分信息不准确。
⑧https://www.freie-messenger.de/xmpp/server/
> 显示服务器的一些策略等其他信息。服务器能用，一些信息不准确。
⑨https://status.conversations.im/historical/
> 一些服务器的正常运行时间数据。

.note #xmppa
XMPP Android 客户端
> 曾经使用过好多，说几个常见的吧。

①Conversations
官网：https://conversations.im/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/eu.siacs.conversations/
Google play 下载地址：https://play.google.com/store/apps/details?id=eu.siacs.conversations
> 有中文。Google play付费版相当于捐钱给开发者，经常限免。简单说下区别，play版从2.12.7开始删除频道发现功能，好处是能加入测试，更新频繁，经常反馈错误。新用户友好，功能较少，问题很少，75%的用户使用F-droid版，日常使用首选。

②Cheogram
官网：https://cheogram.com/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/com.cheogram.android/
Google play 下载地址：https://play.google.com/store/apps/details?id=com.cheogram.android.playstore
> 有中文。Google play付费版相当于买1个月的 JMP.chat 服务。推荐使用F-Droid版。有一些更改和附加功能，更新频繁，问题不多，日常使用备选。

③monocles chat
官网：https://monocles.de/more/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/de.monocles.chat/
Google play 下载地址：https://play.google.com/store/apps/datasafety?id=de.monocles.chat
> 有中文。基于blabber.im和Conversations，有很多更改和附加功能，更新频繁，问题稍多，容易卡住，日常使用备选。

④blabber.im
官网：https://blabber.im/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/de.pixart.messenger/
> 有中文。基于Conversations，有一些更改和附加功能。目前已停止开发，请谨慎使用。

⑤aTalk
官网：https://atalk.sytes.net/atalk/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/org.atalk.android/
Google play 下载地址：https://play.google.com/store/apps/details?id=org.atalk.android/
> 有中文。可能有用户无法成功登录，有好多功能，账号无法成功登录的用户就别试了，更新频繁，问题稍多，容易卡住。

⑥yaxim
官网：https://yaxim.org/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/org.yaxim.androidclient/
Google play 下载地址：https://play.google.com/store/apps/details?id=org.yaxim.androidclient
https://play.google.com/store/apps/details?id=org.yaxim.bruno
> 有中文。Bruno the Jabber Bear 只是 yaxim 换个主题，开发缓慢，功能简单，简单聊天足够。

⑦Xabber
官网：https://www.xabber.com/
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/com.xabber.android/
Android Dev版下载地址：https://www.xabber.com/rel/client/android/last/xabber.apk
iOS Alpha版：https://testflight.apple.com/join/s5uARgJ6
> 有中文。Xabber曾是Android上最流行的客户端，仅Google play下载100多万，不包含Classic版、Beta版、Dev版、VIP版以及F-Droid的所有版本。目前是半成熟产品，因为开发者坚持要放弃当前使用的一些协议，研究自己的，与当前XMPP功能不完全兼容，功能较少，有一些特色功能，开发缓慢，简单聊天足够。

⑧Stork IM
官网：https://stork.im/
F-Droid 下载地址：https://f-droid.org/en/packages/org.tigase.messenger.phone.pro/
Google play 下载地址：https://play.google.com/store/apps/details?id=org.tigase.messenger.phone.pro
> 无中文。据说是与 Tigase 使用很好，开发缓慢，功能较少，使用后感觉太差了，很卡，不建议日常使用。

⑨BombusMod
F-Droid 下载地址：https://f-droid.org/zh_Hans/packages/org.bombusmod/
Google play 下载地址：https://play.google.com/store/apps/details?id=org.bombusmod
> 无中文。基于 J2ME 应用程序的全功能 XMPP 客户端，他们自己说的。仅简单维护，功能确实挺多，很卡，不建议日常使用。

⑩jTalk Messenger
Google play 下载地址：https://play.google.com/store/apps/details?id=com.jtalk2
> 无中文。全功能的 Jabber 客户端，他们自己说的。可能停止维护，功能确实多了点，有点卡，不建议日常使用。

.note #xmppw
XMPP Web 客户端

①Converse
官方实例：https://conversejs.org/fullscreen.html
群主自己也搭了一个，大家可以试试：https://wtfipfs.eu.org/xmpp/
> 有中文，没找到怎么设置就用浏览器翻译吧。功能挺多，需要服务器支持。很多管理员也会提供这个，去相应的网站寻找。

②Movim
> Movim 是一个社交和聊天平台，充当 XMPP 网络的前端，功能好多，非常棒。
此处列出一些实例：https://join.movim.eu/
这是官方实例：https://mov.im/login
> 有中文，部分功能需要服务器支持，某些旧版服务器无法使用正常功能。登录账号后一直在线，需要手动设置。如果不再使用此实例，选择离开实例，删除在此实例的数据。不要选择删除账号，否则会从服务器中注销自己账号！

③Xabber
https://web.xabber.com
开发版地址：https://web.xabber.com/develop/
> 有中文，看起来不错，好多功能与当前使用的XMPP不一致，有中文，有一些特色功能，与当前XMPP好多不兼容，经常更新。感兴趣的试试。

④JSXC
https://www.jsxc.org/example/
https://github.com/jsxc/jsxc
> 有中文。更多信息见相关网站

⑤Candy
https://candy-chat.github.io/candy/
https://github.com/candy-chat/candy
> 有中文。更多信息见相关网站

.note #xmppo
XMPP 其他客户端

①Gajim
官网：https://gajim.org/
下载地址：https://gajim.org/download/
> 有中文。适用于 Windows、MacOS 和 Linux 。新用户友好，功能稍多，也会崩溃，还不错，日常使用首选。

②Dino
官网：https://dino.im/
下载地址：https://github.com/dino/dino/wiki/Distribution-Packages
第三方也支持Windows：https://github.com/LAGonauta/dino
> 有中文。官方支持 Linux。新用户友好，功能较少，也会崩溃，还不错。Gajim不支持视频通话，Dino支持，两者搭配使用更好。

③Psi 与 Psi+
Psi 官网：https://psi-im.org/
Psi+ 官网：https://psi-plus.com/
下载地址：https://sourceforge.net/projects/psiplus/
> 有中文。适用于 Windows、MacOS 和 Linux。Psi 专为经验丰富的用户而设计。发布的版本相当少见。Psi+是 Psi 一个开发分支，可以快速地收到新功能和错误修复。功能好多，虽说是专为经验丰富的用户而设计，高级用户的选择，新用户可以一试。群聊缺少一个比较重要的功能，可能会漏消息，建议与上边某一个搭配使用。

④Monal IM
官网：https://monal-im.org/
iOS 下载地址：https://apps.apple.com/app/id317711500
macOS 下载地址：https://apps.apple.com/app/id1637078500
> iOS 和 macOS XMPP 聊天客户端，我没用过，感兴趣的试试。

⑤Siskin IM
官网：https://siskin.im/
下载地址：https://itunes.apple.com/us/app/tigase-messenger/id1153516838
> 适用于 iPhone 和 iPad 的轻量级且功能强大的 XMPP 客户端，他们自己说的，我没用过，感兴趣的试试。

⑥Beagle IM
官网：https://beagle.im/
下载地址：https://apps.apple.com/us/app/beagleim-by-tigase-inc/id1445349494
> 适用于 MacOS 的轻量级且功能强大的 XMPP 客户端，他们自己说的，我没用过，感兴趣的试试。

⑦Profanity
官网：https://profanity-im.github.io/
> 适用于 Linux、FreeBSD、OpenBSD、OSX、Windows 和 Android（Termux）控制台客户端。功能丰富，感兴趣的试试。更多信息见相关网站。

⑧Poezio
官网：https://poez.io/en/
> 和上边一样，自行体验。

⑨MCABBER
官网：https://mcabber.com/
> 和上边一样，自行体验。

⑩Pidgin
官网：https://pidgin.im/
> 有中文，可以在 Windows、Linux 和其他类 UNIX 操作系统上运行。 与很多聊天网络兼容，功能好多。但对于XMPP，能基本聊天，问题多。

⑪Adium
官网：https://adium.im/
> 适用于 MacOS 的免费即时通讯应用程序，可以连接到 XMPP/Jabber、IRC 等。 但对于XMPP，能满足基本的聊天。

⑫CoyIM
官网：https://coy.im/
> 适用于 Windows、MacOS 和 Linux 。功能较少。

⑬Swift
官网：https://swift.im/index.html
> 适用于 Windows、MacOS 和 Linux 。功能较少。

⑭UWPX
官网：https://uwpx.org/
> 适用于 UWP（Windows 10 和 Windows 11）。功能较少。

⑮Kaidan
官网：https://www.kaidan.im/
> 适用于Linux、Windows、MacOS、Android、Plasma Mobile 和 Ubuntu Touch。不幸的是，目前无法为所有平台提供构建，由于开发者资源很少。功能较少。

⑯AstraChat
官网：https://astrachat.com/
> AstraChat Mobile 专为 Android、BlackBerry 10 和 Apple iOS 设备而设计。AstraChat Desktop 适用于 Windows、Linux 和 Mac。功能较少。

> 上边只是列出一些常见的客户端，仅供参考，喜欢的话可以给他们捐款！

https://xmpp.org/software/?platform=all-platforms
> 在此部分中，将找到有关 XMPP 软件的信息，包括客户端、服务器、库等。

.note #xmppp
XMPP 提供者
喜欢的话可以给他们捐款，请不要滥用！！！
> 公共服务器数量由少到多（Tigase-ejabberd-Prosody），有的数量太少（Metronome、Openfire），不列出。
> 相关统计：https://search.jabber.network/stats
> 付费，关闭注册，仅邀请注册，404.city、suchat.org等强制需要验证邮箱账号的不列出。
> 大部分不需要提交电子邮件账号，有的只提交不验证，Tigase 全需要验证，列出供大家体验。
> 像riseup、calyx那种，一直提示用户发送加密消息，很烦人的，不列出。由用户自己决定是否加密。
> 部分服务器能屏蔽陌生人，有的只能屏蔽非本服务器的。比如404.city、suchat.org。推荐用户优先注册ejabberd服务器。Prosody某些功能取决于服务器管理员，不好评价。Tigase 仅供用户测试，不是很推荐注册使用。部分客户端能设置反垃圾，或者忽略不在联系人列表中的一切活动，或者使用隐私列表，不要过分依赖服务器。Gajim 1.2.1及以后的版本不支持XEP-0016。遇到大量垃圾消息骚扰，Gajim账号设置 隐私 忽略未知联系人。或者 Gajim 插件 下载Anti-Spam，配置一下。一般是不需要这样做。其他客户端支持XEP-0016，能添加更多规则。我的建议是不会配置XEP-0016规则就不要设置这些，比较复杂，影响正常使用。XEP-0191更简单方便，但功能更少。Conversations 用户关闭陌生人的通知后，只能一个一个再屏蔽了，如果服务器支持顺便举报这些账号。

①Tigase（功能丰富，版本一样，免费托管域名）
https://sure.im
https://tigase.im
https://tigase.eu
https://tigase.me
https://tigase.chat
https://xmpp.cloud
https://jabber.today
域名相关配置文档
https://docs.tigase.net/en/latest/Tigase_Administration/Quick_Start_Guide/Intro.html#hosting-via-tigase-me

②ejabberd（功能丰富，版本不同）
xmpp:conversations.im?register
xmpp:nixnet.services?register
xmpp:paranoid.network?register
xmpp:linux.monster?register
xmpp:pwned.life?register
xmpp:draugr.de?register
xmpp:deshalbfrei.org?register
xmpp:ubuntu-jabber.de?register
xmpp:ubuntu-jabber.net?register
xmpp:verdammung.org?register
xmpp:xabber.de?register
xmpp:chapril.org?register
xmpp:chalec.org?register
xmpp:yourdata.forsale?register
xmpp:magicbroccoli.de?register
xmpp:macaw.me?register
xmpp:projectsegfau.lt?register
xmpp:redlibre.es?register
xmpp:libretank.org?register
xmpp:chat.sum7.eu?register
xmpp:hookipa.net?register
xmpp:xmpp.social?register
xmpp:chat.sum7.eu?register
xmpp:marxist.club?register
xmpp:07f.de?register
xmpp:chatterboxtown.us?register
https://www.jabjab.de/register
https://www.xmpp.jp/signup
https://join.movim.eu/register
https://jabb.im/reg/
https://anoxinon.de/dienste/anoxinonmessenger/
https://jabber.tcpreset.net:5280/register/new
https://jabber.systemausfall.org/register/new
https://laberzentrale.de/register
https://elaon.de/dienste/xmpp/
https://jabbxi.de/register
提供好多域名，感兴趣的去网站：https://jabb.im/reg/
提供好多域名，感兴趣的去网站：https://www.shad0w.io/register.php
cn域名，服务器在香港。xmpp:xmpp.cn?register
tw域名，服务器在德国。xmpp:xmpp.tw?register
tw域名，服务器在德国。xmpp:jabber.tw?register
上边这3个都是由 jabberx 提供的，还提供了好多域名，感兴趣的去网站：https://jabberx.com/

③Prosody（功能丰富，版本不同）
xmpp:yax.im?register
xmpp:jabbers.one?register
xmpp:anonym.im?register
xmpp:xmpp.earth?register
xmpp:loqi.im?register
https://wiuwiu.de/en/#register
https://pimux.de/registration
https://5222.de/register
https://xmpp.is/account/register/
https://www.jabber-germany.de/register.html
xmpp:jabber.fr?register
除jabber.fr外还提供好多域名，感兴趣的去网站：https://jabberfr.org/inscription
提供好多域名，感兴趣的去网站：https://xmpp.is/account/register/xmpp_is
提供好多域名，感兴趣的去网站：https://jabber.hot-chilli.net/forms/create/#new_tab

> 所有服务器或客户端都有优缺点，请自行体验！
> 以上所有评论仅代表个人看法，请自行体验！
> 上述服务器的策略、条款、隐私，请自行查阅！
> 按原样提供，风险自负，不提供任何担保或保证！