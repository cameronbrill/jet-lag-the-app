import Shared
import SwiftUI

@main
struct JetLagIOSApp: App {
    var body: some Scene {
        WindowGroup {
            ComposeRootView()
        }
    }
}

struct ComposeRootView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> UIViewController {
        MainKt.mainViewController()
    }

    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {}
}
