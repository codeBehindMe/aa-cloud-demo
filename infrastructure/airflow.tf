//resource "google_composer_environment" "qa_composer" {
//  name = "qa-composer-env"
//  region = var.deploy_region
//
//  config {
//    node_count = 4
//
//    node_config {
//      zone = var.deploy_zone
//      machine_type = "n1-standard-1"
//
//      network = google_compute_network.vpc_network.self_link
//      subnetwork = google_compute_subnetwork.qa-airflow.self_link
//    }
//
//  }
//}

resource "google_composer_environment" "qa-airflow" {
  name = "qa-composer"
  region = var.deploy_region
}