#概要
GAE(Google App Engine)をproxyサーバとして利用するアプリ
ブラウザから指定されたURLをGAEのURLFetchを使い取得し、内容をUTF-8に変換してクライアントに返す
ことで文字化けを防いだり、URLフィルタリングにかかるサイトを回避する。
またクライアント側ではリンクのURLをJavaScriptでproxyサーバを経由するように書き換えることで
リンクをクリックしてもproxyが使われ続けるようにする。

#実際のサイト
http://weightmange.appspot.com/main 