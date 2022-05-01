//
//  ContentView.swift
//  Nimbus Expenses
//
//  Created by Sam Bradshaw on 1/5/2022.
//

import SwiftUI
import UIKit
import WebKit

struct WebView: UIViewRepresentable {
    typealias UIViewType = WKWebView

    let webView: WKWebView
    
    func makeUIView(context: Context) -> WKWebView {
        return webView
    }
    
    func updateUIView(_ uiView: WKWebView, context: Context) { }
}


class WebViewModel: ObservableObject {
    let webView: WKWebView
    let url: URL
    
    init() {
        webView = WKWebView(frame: .zero)
        url = URL(string: "https://benoitpasquier.com")!

        loadUrl()
    }
    
    func loadUrl() {
        webView.load(URLRequest(url: url))
    }
}

struct ContentView: View {
    
    @StateObject var model = WebViewModel()
    
    var body: some View {
        WebView(webView: model.webView)
    }
}
                  
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
