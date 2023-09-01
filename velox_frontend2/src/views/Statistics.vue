<template>
  <div>
    <b-row>
      <b-colxx xxs="12">
        <div class="separator mb-5"></div>
      </b-colxx>
    </b-row>
    <b-row>
      <b-colxx xxs="12">
        <h4 class="card-title">Statistics</h4>
        <b-tabs content-class="mt-3">
          <b-tab title="Population" active>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <PopulationWithBiomechanics :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <PopulationWithCardio :result1="result1" />
              </div>
            </div>
          </b-tab>
          <b-tab title="Biomechanics">
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <BiomechanicsScoreByAge :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <BiomechanicsScoreByCluster :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div class="row">
                <div class="col-lg-1"></div>
                <div class="col-lg-10">
                  <div v-if="loading" class="loader">
                    <svg
                      width="200px"
                      height="200px"
                      xmlns="http://www.w3.org/2000/svg"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      viewBox="0 0 100 100"
                      preserveAspectRatio="xMidYMid"
                      style="background: none;"
                    >
                      <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.875s"
                        ></animate>
                      </circle>
                      <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.75s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.625s"
                        ></animate>
                      </circle>
                      <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.5s"
                        ></animate>
                      </circle>
                      <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.375s"
                        ></animate>
                      </circle>
                      <circle
                        cx="32.322"
                        cy="32.322"
                        fill="#363a3c"
                        r="4.80282"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.25s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.125s"
                        ></animate>
                      </circle>
                      <circle
                        cx="67.678"
                        cy="32.322"
                        fill="#363a3c"
                        r="7.99718"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="0s"
                        ></animate>
                      </circle>
                    </svg>
                  </div>
                  <div v-else>
                    <h5 class="text-center">
                      Biomechanics Score by Horse Type
                    </h5>
                    <BiomechanicsScoreByType :result1="result1" />
                  </div>
                </div>
                <div class="col-lg-1"></div>
              </div>
            </div>
          </b-tab>
          <b-tab title="Conformation">
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <ConformationScoreByAge :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div class="row">
                <div class="col-lg-1"></div>
                <div class="col-lg-10">
                  <div v-if="loading" class="loader">
                    <svg
                      width="200px"
                      height="200px"
                      xmlns="http://www.w3.org/2000/svg"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      viewBox="0 0 100 100"
                      preserveAspectRatio="xMidYMid"
                      style="background: none;"
                    >
                      <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.875s"
                        ></animate>
                      </circle>
                      <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.75s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.625s"
                        ></animate>
                      </circle>
                      <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.5s"
                        ></animate>
                      </circle>
                      <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.375s"
                        ></animate>
                      </circle>
                      <circle
                        cx="32.322"
                        cy="32.322"
                        fill="#363a3c"
                        r="4.80282"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.25s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.125s"
                        ></animate>
                      </circle>
                      <circle
                        cx="67.678"
                        cy="32.322"
                        fill="#363a3c"
                        r="7.99718"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="0s"
                        ></animate>
                      </circle>
                    </svg>
                  </div>
                  <div v-else>
                    <h5 class="text-center">
                      Conformation Score by Horse Type
                    </h5>
                    <ConformationScoreByType :result1="result1" />
                  </div>
                </div>
                <div class="col-lg-1"></div>
              </div>
            </div>
          </b-tab>
          <b-tab title="The Shortlist">
            <div class="chart">
                <TheShortlist/>
              <hr />
            </div>
          </b-tab>
          <b-tab title="Cardio">
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <CardioScoreByAge :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <CardioScoreByCluster :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <CardioScoreByType :result1="result1" />
              </div>
            </div>
          </b-tab>
          <b-tab title="Cardio + Biomechanics">
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <CardioBiomechanicsScoreByAge :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div class="row">
                <div class="col-lg-1"></div>
                <div class="col-lg-10">
                  <div v-if="loading" class="loader">
                    <svg
                      width="200px"
                      height="200px"
                      xmlns="http://www.w3.org/2000/svg"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      viewBox="0 0 100 100"
                      preserveAspectRatio="xMidYMid"
                      style="background: none;"
                    >
                      <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.875s"
                        ></animate>
                      </circle>
                      <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.75s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.625s"
                        ></animate>
                      </circle>
                      <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.5s"
                        ></animate>
                      </circle>
                      <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.375s"
                        ></animate>
                      </circle>
                      <circle
                        cx="32.322"
                        cy="32.322"
                        fill="#363a3c"
                        r="4.80282"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.25s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.125s"
                        ></animate>
                      </circle>
                      <circle
                        cx="67.678"
                        cy="32.322"
                        fill="#363a3c"
                        r="7.99718"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="0s"
                        ></animate>
                      </circle>
                    </svg>
                  </div>
                  <div v-else>
                    <h5 class="text-center">
                      Cardio + Biomechanics Score by Horse Type
                    </h5>
                    <CardioBiomechanicsScoreByType :result1="result1" />
                  </div>
                </div>
                <div class="col-lg-1"></div>
              </div>
            </div>
          </b-tab>
          <b-tab title="DNA + Cardio + Biomechanics">
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <DNACardioBiomechanicsScoreByAge :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div class="row">
                <div class="col-lg-1"></div>
                <div class="col-lg-10">
                  <div v-if="loading" class="loader">
                    <svg
                      width="200px"
                      height="200px"
                      xmlns="http://www.w3.org/2000/svg"
                      xmlns:xlink="http://www.w3.org/1999/xlink"
                      viewBox="0 0 100 100"
                      preserveAspectRatio="xMidYMid"
                      style="background: none;"
                    >
                      <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.875s"
                        ></animate>
                      </circle>
                      <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.75s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.625s"
                        ></animate>
                      </circle>
                      <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.5s"
                        ></animate>
                      </circle>
                      <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.375s"
                        ></animate>
                      </circle>
                      <circle
                        cx="32.322"
                        cy="32.322"
                        fill="#363a3c"
                        r="4.80282"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.25s"
                        ></animate>
                      </circle>
                      <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="-0.125s"
                        ></animate>
                      </circle>
                      <circle
                        cx="67.678"
                        cy="32.322"
                        fill="#363a3c"
                        r="7.99718"
                      >
                        <animate
                          attributeName="r"
                          values="4.8;4.8;8;4.8;4.8"
                          times="0;0.1;0.2;0.3;1"
                          dur="1s"
                          repeatCount="indefinite"
                          begin="0s"
                        ></animate>
                      </circle>
                    </svg>
                  </div>
                  <div v-else>
                    <h5 class="text-center">
                      DNA + Cardio + Biomechanics Score by Horse Type
                    </h5>
                    <DNACardioBiomechanicsScoreByType :result1="result1" />
                  </div>
                </div>
                <div class="col-lg-1"></div>
              </div>
            </div>
          </b-tab>
          <b-tab title="Model Evaluation">
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <BiomechanicsModelEvalution :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <ConformationModelEvalution :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <CardioBiomechanicsModelEvalution :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <DNACardioBiomechanicsModelEvalution :result1="result1" />
              </div>
              <hr />
            </div>
            <div class="chart">
              <div v-if="loading" class="loader">
                <svg
                  width="200px"
                  height="200px"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  viewBox="0 0 100 100"
                  preserveAspectRatio="xMidYMid"
                  style="background: none;"
                >
                  <circle cx="75" cy="50" fill="#363a3c" r="6.39718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.875s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.75s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="75" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.625s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="67.678" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.5s"
                    ></animate>
                  </circle>
                  <circle cx="25" cy="50" fill="#363a3c" r="4.8">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.375s"
                    ></animate>
                  </circle>
                  <circle cx="32.322" cy="32.322" fill="#363a3c" r="4.80282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.25s"
                    ></animate>
                  </circle>
                  <circle cx="50" cy="25" fill="#363a3c" r="6.40282">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="-0.125s"
                    ></animate>
                  </circle>
                  <circle cx="67.678" cy="32.322" fill="#363a3c" r="7.99718">
                    <animate
                      attributeName="r"
                      values="4.8;4.8;8;4.8;4.8"
                      times="0;0.1;0.2;0.3;1"
                      dur="1s"
                      repeatCount="indefinite"
                      begin="0s"
                    ></animate>
                  </circle>
                </svg>
              </div>
              <div v-else>
                <OptimalDistanceModelEvalution :result1="result1" />
              </div>
            </div>
          </b-tab>
        </b-tabs>
      </b-colxx>
    </b-row>
  </div>
</template>
<script>
import PopulationWithBiomechanics from "../chart/PopulationWithBiomechanics";
import PopulationWithCardio from "../chart/PopulationWithCardio";
import CardioScoreByAge from "../chart/CardioScoreByAge";
import CardioScoreByCluster from "../chart/CardioScoreByCluster";
import CardioScoreByType from "../chart/CardioScoreByType";
import BiomechanicsScoreByAge from "../chart/BiomechanicsScoreByAge";
import BiomechanicsScoreByCluster from "../chart/BiomechanicsScoreByCluster";
import BiomechanicsScoreByType from "../chart/BiomechanicsScoreByType";
import ImageScoreByAge from "../chart/ImageScoreByAge";
import ImageScoreByCluster from "../chart/ImageScoreByCluster";
import ImageScoreByType from "../chart/ImageScoreByType";
import CardioBiomechanicsScoreByAge from "../chart/CardioBiomechanicsScoreByAge";
import CardioBiomechanicsScoreByType from "../chart/CardioBiomechanicsScoreByType";
import DNACardioBiomechanicsScoreByAge from "../chart/DNACardioBiomechanicsScoreByAge";
import ConformationScoreByAge from "../chart/ConformationScoreByAge";
import ConformationScoreByType from "../chart/ConformationScoreByType";
import DNACardioBiomechanicsScoreByType from "../chart/DNACardioBiomechanicsScoreByType";
import BiomechanicsModelEvalution from "../chart/BiomechanicsModelEvalution";
import ConformationModelEvalution from "../chart/ConformationModelEvalution";
import OptimalDistanceModelEvalution from "../chart/OptimalDistanceMoelEvalution";
import CardioBiomechanicsModelEvalution from "../chart/CardioBiomechanicsModelEvalution";
import DNACardioBiomechanicsModelEvalution from "../chart/DNACardioBiomechanicsModelEvalution";
import TheShortlist from "../chart/TheShortlist";
import api from "@/services/axios";

export default {
  name: "Statistics",
  components: {
    PopulationWithBiomechanics,
    PopulationWithCardio,
    CardioScoreByAge,
    CardioScoreByCluster,
    CardioScoreByType,
    BiomechanicsScoreByAge,
    BiomechanicsScoreByCluster,
    BiomechanicsScoreByType,
    ImageScoreByAge,
    ImageScoreByCluster,
    ImageScoreByType,
    CardioBiomechanicsScoreByAge,
    CardioBiomechanicsScoreByType,
    DNACardioBiomechanicsScoreByAge,
    DNACardioBiomechanicsScoreByType,
    BiomechanicsModelEvalution,
    ConformationModelEvalution,
    OptimalDistanceModelEvalution,
    CardioBiomechanicsModelEvalution,
    DNACardioBiomechanicsModelEvalution,
    ConformationScoreByAge,
    ConformationScoreByType,
    TheShortlist
  },
  data() {
    return {
      result1: [],
      loading: false
    };
  },
  async mounted() {
    this.loading = true;
    api
      .get(`/horses/stats/`)
      .then(response => {
        this.result1 = response;
      })
      .catch(error => {})
      .finally(() => (this.loading = false));
  }
};
</script>

<style>
.chart {
  margin-top: 50px;
}
.loader {
  text-align: center;
}
</style>
