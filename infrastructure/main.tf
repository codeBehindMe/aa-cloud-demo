provider "google" {
  project = "aa-cc-dem"
  region = var.deploy_region
  zone = var.deploy_zone
}

resource "google_container_cluster" "primary" {
  name = "worker-cluster"
  location = var.deploy_zone
  remove_default_node_pool = true
  initial_node_count = 1
  network = google_compute_network.vpc_network.self_link

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name = "preemptible-node-pool"
  cluster = google_container_cluster.primary.name
  location = var.deploy_zone
  node_count = 3

  node_config {
    preemptible = true
    machine_type = "n1-standard-1"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
  auto_create_subnetworks = "true"

}

