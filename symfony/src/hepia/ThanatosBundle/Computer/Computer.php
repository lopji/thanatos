<?php

namespace hepia\ThanatosBundle\Computer;

use ElephantIO\Client;
use ElephantIO\Engine\SocketIO\Version1X;
use ElephantIO\Exception\ServerConnectionFailureException;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * Description of Computer
 *
 * @author rocha
 */
class Computer {

    private $ip_server;

    public function __construct($ip_server) {
        $this->ip_server = $ip_server;
    }

    public function getAvailable() {
        $client = new Client(new Version1X($this->ip_server));
        $computers = array();
        try {
            $client->initialize();
            $client->of('/php');
            $client->emit("available", array());
            $data1 = $client->read();
            $data2 = $client->read();
            if ($data1 == "40/php") {
                $data = json_decode(substr($data2, 7, strlen($data2)));
                foreach ($data[1] as $value) {
                    $computers[$value->name] = $value->name;
                }
            }
            $client->close();
        } catch (ServerConnectionFailureException $e) {
            
        }
        return $computers;
    }

    public function launch($id, $name) {
        $client = new Client(new Version1X($this->ip_server));
        try {
            $client->initialize();
            $client->of('/php');
            $client->emit("launch", ['id' => $id, 'name' => $name]);
            $client->close();
        } catch (ServerConnectionFailureException $e) {
            
        }
    }

}
